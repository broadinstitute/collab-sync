"""Command-line interface for collab-sync."""

from pathlib import Path

import typer

from .catalog import generate_catalog
from .sync import sync_collaborators
from .visibility import update_visibility

app = typer.Typer(help="GitHub collaborator and repository management for consortiums")


@app.command()
def sync(
    config_dir: Path = typer.Option(Path("."), "--config-dir", "-c", help="Directory containing YAML config files"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview changes without applying them"),
):
    """Sync GitHub collaborators from YAML configuration."""
    sync_collaborators(config_dir, dry_run)


@app.command()
def update(
    config_dir: Path = typer.Option(Path("."), "--config-dir", "-c", help="Directory containing YAML config files"),
):
    """Update repository visibility from GitHub."""
    update_visibility(config_dir)


@app.command()
def catalog(
    config_dir: Path = typer.Option(Path("."), "--config-dir", "-c", help="Directory containing YAML config files"),
):
    """Generate repository catalog page."""
    generate_catalog(config_dir)


if __name__ == "__main__":
    app()
