"""Sync GitHub collaborators from YAML configuration."""

import json
import logging
import subprocess
import sys
from pathlib import Path

import yaml

# Configure logging with cleaner console output
logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s", stream=sys.stdout)
logger = logging.getLogger(__name__)


def gh_error(result: subprocess.CompletedProcess) -> str:
    """Return gh's one-line summary (stderr) plus GitHub's response body (stdout), which carries the actual reason."""
    return f"{result.stderr.strip()} {result.stdout.strip()}"


def delete_expired_invitations(org: str, repo: str, dry_run: bool = False) -> None:
    """Delete expired invitations for a repository."""
    cmd = ["gh", "api", f"repos/{org}/{repo}/invitations", "--paginate"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"Failed to get invitations for {repo}: {gh_error(result)}")
        return

    invitations = json.loads(result.stdout)
    expired_count = 0

    for invitation in invitations:
        if invitation.get("expired"):
            username = invitation["invitee"]["login"]
            invitation_id = invitation["id"]
            expired_count += 1

            if dry_run:
                logger.info(f"Would delete expired invitation: {username} <- {repo} (ID: {invitation_id})")
            else:
                delete_cmd = ["gh", "api", f"repos/{org}/{repo}/invitations/{invitation_id}", "-X", "DELETE"]
                delete_result = subprocess.run(delete_cmd, capture_output=True, text=True)
                if delete_result.returncode == 0:
                    logger.info(f"✓ Deleted expired invitation: {username} <- {repo}")
                else:
                    logger.error(f"✗ Failed to delete invitation for {username} <- {repo}: {gh_error(delete_result)}")

    if expired_count == 0:
        logger.info(f"No expired invitations for {repo}")


def sync_collaborators(config_dir: Path, dry_run: bool = False, resend_expired: bool = False) -> None:
    """Sync collaborators for a GitHub organization from YAML config."""
    # Load YAML
    config_path = config_dir / "collaborators.yaml"
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)

    with config_path.open() as f:
        data = yaml.safe_load(f)

    org = data.get("organization")
    if not org:
        logger.error("Missing 'organization' field in collaborators.yaml")
        sys.exit(1)

    collaborators = data.get("collaborators", [])
    protected_admins = data.get("protected_admins", [])
    managed_repos = data.get("managed_repos", [])
    has_errors = False

    logger.info(f"Organization: {org}")
    logger.info(f"Protected admins: {', '.join(protected_admins)}")
    logger.info(f"Managed repos: {', '.join(managed_repos)}")
    if dry_run:
        logger.info("🔍 DRY RUN MODE - No changes will be made")

    # Delete expired invitations if requested
    if resend_expired:
        logger.info("Checking for expired invitations...")
        all_repos = set(managed_repos) if managed_repos else set()
        for c in collaborators:
            permissions = c.get("permissions", {})
            for repo in permissions.keys():
                all_repos.add(repo)

        for repo in all_repos:
            delete_expired_invitations(org, repo, dry_run)

    # IMPORTANT: Ensure all collaborators FIRST before removing anyone
    # This prevents accidentally locking ourselves out
    logger.info("Syncing collaborator permissions...")
    for collab in collaborators:
        username = collab["username"]
        permissions = collab.get("permissions", {})

        for repo, permission in permissions.items():
            if dry_run:
                logger.info(f"Would sync: {username} -> {repo} ({permission})")
            else:
                cmd = ["gh", "api", f"repos/{org}/{repo}/collaborators/{username}", "-X", "PUT", "-f", f"permission={permission}"]
                logger.info(f"Running: {cmd}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"✓ Synced {username} -> {repo} ({permission})")
                else:
                    logger.error(f"✗ Failed to sync {username} -> {repo}: {gh_error(result)}")
                    has_errors = True

    # Remove unlisted collaborators (after ensuring we have access)
    logger.info("Removing unlisted direct collaborators (ignoring team members)...")

    # Build sets of all repos and expected collaborator/repo pairs
    all_repos = set(managed_repos) if managed_repos else set()
    expected = set()

    for c in collaborators:
        username = c["username"]
        permissions = c.get("permissions", {})
        for repo in permissions.keys():
            all_repos.add(repo)
            expected.add((username, repo))

    for repo in all_repos:
        # Get current direct collaborators only (not team members)
        cmd = ["gh", "api", f"repos/{org}/{repo}/collaborators?affiliation=direct", "--paginate"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            current = json.loads(result.stdout)
            for user in current:
                username = user["login"]
                if (username, repo) not in expected:
                    # Never remove protected admins
                    if username in protected_admins:
                        logger.warning(f"Skipping protected admin: {username} <- {repo}")
                        continue

                    if dry_run:
                        logger.info(f"Would remove: {username} <- {repo}")
                    else:
                        cmd = ["gh", "api", f"repos/{org}/{repo}/collaborators/{username}", "-X", "DELETE"]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode == 0:
                            logger.info(f"✓ Removed {username} <- {repo}")
                        else:
                            logger.error(f"✗ Failed to remove {username} <- {repo}: {gh_error(result)}")
                            has_errors = True
        else:
            logger.error(f"Failed to get collaborators for {repo}: {gh_error(result)}")
            has_errors = True

    if dry_run:
        logger.info("🔍 Dry run completed - no changes were made")
    elif has_errors:
        logger.error("❌ Sync completed with errors")
        sys.exit(1)
    else:
        logger.info("✅ Sync completed successfully")
