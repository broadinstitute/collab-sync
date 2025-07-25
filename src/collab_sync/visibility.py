"""Update repository visibility status from GitHub API."""

import json
import subprocess
from pathlib import Path

import yaml


def get_repo_visibility(org: str, repo_name: str) -> str | None:
    """Get repository visibility from GitHub API using gh CLI."""
    try:
        result = subprocess.run(["gh", "api", f"repos/{org}/{repo_name}"], capture_output=True, text=True, check=True)
        repo_data = json.loads(result.stdout)
        return "private" if repo_data["private"] else "public"
    except subprocess.CalledProcessError:
        print(f"Warning: Could not fetch data for {repo_name}")
        return None


def update_visibility(org: str, config_dir: Path) -> None:
    """Update repository visibility from GitHub API."""
    # Load current YAML
    repos_path = config_dir / "repositories.yaml"
    if not repos_path.exists():
        print(f"Configuration file not found: {repos_path}")
        return

    with repos_path.open() as f:
        data = yaml.safe_load(f)

    updated = False

    # Update visibility for each repository
    for repo in data["repositories"]:
        repo_name = repo["name"]
        current_visibility = repo.get("visibility", "unknown")

        # Fetch actual visibility from GitHub
        actual_visibility = get_repo_visibility(org, repo_name)

        if actual_visibility and actual_visibility != current_visibility:
            print(f"Updating {repo_name}: {current_visibility} → {actual_visibility}")
            repo["visibility"] = actual_visibility
            updated = True
        elif actual_visibility:
            print(f"✓ {repo_name}: {actual_visibility}")

    # Save updated YAML if changes were made
    if updated:
        with repos_path.open("w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
        print(f"\n{repos_path} updated!")
    else:
        print("\nNo updates needed.")
