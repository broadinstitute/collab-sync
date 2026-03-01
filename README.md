# collab-sync

GitHub collaborator and repository management for consortiums.

## Why collab-sync?

Research consortiums often span multiple institutions, with external collaborators who need access to specific repositories within an existing GitHub organization. The two obvious GitHub solutions don't work well here:

- **Teams** — GitHub Teams [cannot include outside collaborators](https://github.com/orgs/community/discussions/174719); only organization members can be added to teams. For consortiums where most participants are external, this rules out teams as an access-management tool.
- **Separate organization** — Creating a dedicated org gives full control but adds significant overhead: another org to administer, separate billing, and collaborators scattered across orgs.

`collab-sync` takes a lighter approach: stay within the existing org and manage **direct collaborator** invitations per-user, per-repo. A YAML file declares who gets `pull`, `push`, or `admin` access to which repos, and a sync command applies it via the GitHub API. Because the desired state lives in YAML checked into git, every access change is reviewable in a PR, visible in the commit history, and easy to roll back.

If GitHub Teams eventually allows outside collaborators to join teams, much of the need for this tool goes away and we may deprecate it in favor of native team-based access control.

**Scope:** `collab-sync` does three things — sync collaborator permissions, track repository visibility, and generate a catalog page. It deliberately does not manage repo settings, branch protections, org policies, or anything beyond access and discovery. Keeping the scope narrow avoids feature creep and keeps the tool easy to reason about.

## Overview

`collab-sync` provides a simple, declarative way to manage GitHub collaborators and maintain repository catalogs across multiple organizations. It uses YAML configuration files to define the desired state and syncs it with GitHub.

## How It Works

`collab-sync` uses a **dual-authority model** — each config file has a clear source of truth so changes always flow in one direction:

| File | Source of truth | Sync direction |
| ---- | --------------- | -------------- |
| `collaborators.yaml` | **YAML** (this file) | YAML → GitHub — edits here are pushed to GitHub; manual GitHub changes are overridden |
| `repositories.yaml` | **GitHub** | GitHub → YAML — repository visibility is pulled from GitHub; local edits are overridden |

This means:

- **To change collaborator permissions**, edit `collaborators.yaml` and push. The next sync applies your changes to GitHub.
- **To update the repository catalog**, run `collab-sync update`. It reads current visibility from GitHub and writes it back to `repositories.yaml`.
- Only **direct collaborators** are managed (not organization team members).

## Installation

No installation needed - use directly with `uvx`:

```bash
# From GitHub
uvx --from git+https://github.com/broadinstitute/collab-sync.git collab-sync --help

# From local clone
uvx --from /path/to/collab-sync collab-sync --help
```

## Commands

```bash
# Sync collaborator permissions
collab-sync sync

# Preview changes without applying them
collab-sync sync --dry-run

# Delete and resend expired invitations, then sync
collab-sync sync --resend-expired

# Update repository visibility from GitHub
collab-sync update

# Generate repository catalog page
collab-sync catalog

# Specify custom config directory
collab-sync sync --config-dir /path/to/config
```

## Configuration

Both `collaborators.yaml` and `repositories.yaml` must include an `organization` field specifying your GitHub organization:

```yaml
organization: your-github-org
```

Repositories with `status: planned` are skipped during sync and visibility updates (since they don't exist on GitHub yet). The `catalog` command renders them in a separate "Planned Repositories" section sorted by paper ID.

## Quick Start

To set up `collab-sync` for your consortium:

1. Copy the [`example/`](example/) directory to your new repository
2. Follow the setup instructions in [`example/README.md`](example/README.md)
3. Update the `organization` field in both YAML files
4. Customize the rest of the YAML files for your needs

The example directory contains all needed files and complete setup instructions.

## Requirements

- Python 3.8+
- GitHub CLI (`gh`) installed and authenticated
- GitHub Personal Access Token with `repo` scope (for collaborator management)
