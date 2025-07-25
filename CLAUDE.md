# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

collab-sync is a Python tool for managing GitHub collaborators and repository catalogs across organizations using YAML configuration files. It provides CLI commands to sync collaborators, update repository visibility, and generate catalog pages.

## Development Commands

### Running the CLI locally
```bash
# Using uvx (no installation needed)
uvx --from . collab-sync --help

# Or with pip install in editable mode
pip install -e .
collab-sync --help
```

### Linting and formatting
```bash
# Run ruff linter
ruff check src/

# Run ruff formatter
ruff format src/
```

### Testing commands
```bash
# Test sync with dry-run (no changes)
collab-sync sync --dry-run

# Test with example config
collab-sync sync --config-dir example/
```

## Architecture

The codebase consists of three main modules:

1. **sync.py**: Handles collaborator synchronization between YAML config and GitHub. Uses `gh` CLI to fetch current state and apply changes.

2. **visibility.py**: Updates repository visibility in YAML by fetching current state from GitHub. Note: visibility is read FROM GitHub, not written TO it.

3. **catalog.py**: Generates HTML catalog pages from repository YAML data for GitHub Pages deployment.

All modules rely on:
- YAML files in config directory (`collaborators.yaml` and `repositories.yaml`)
- GitHub CLI (`gh`) for API operations
- Personal Access Token (PAT) for collaborator management

## Key Design Decisions

- Uses `gh` CLI instead of direct API calls for reliability and authentication handling
- YAML files are authoritative for collaborators and descriptions
- Repository visibility is always synced FROM GitHub (never TO)
- Only manages direct collaborators, not team members
- Designed for CI/CD integration with GitHub Actions