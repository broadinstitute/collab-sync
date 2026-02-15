# collab-sync

GitHub collaborator and repository management for consortiums.

## Overview

`collab-sync` provides a simple, declarative way to manage GitHub collaborators and maintain repository catalogs across multiple organizations. It uses YAML configuration files to define the desired state and syncs it with GitHub.

**⚠️ Important:**
- **Collaborators**: User permissions in `collaborators.yaml` → GitHub (yaml is authoritative, GitHub changes overridden)
- **Repository Catalog**: Repository visibility in GitHub → `repositories.yaml` (GitHub is authoritative, yaml changes overridden)
- Only manages direct collaborators (not team members)

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
