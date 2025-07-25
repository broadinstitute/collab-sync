"""Generate a simple markdown page from repositories.yaml."""

from datetime import datetime
from pathlib import Path

import yaml


def generate_catalog(config_dir: Path) -> None:
    """Generate markdown catalog page from repositories.yaml."""
    # Load repository data
    repos_path = config_dir / "repositories.yaml"
    if not repos_path.exists():
        print(f"Configuration file not found: {repos_path}")
        return

    with repos_path.open() as f:
        data = yaml.safe_load(f)

    org = data.get("organization")
    if not org:
        print("Error: Missing 'organization' field in repositories.yaml")
        return

    # Generate markdown content
    content = f"""# Repository Catalog

*Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}*

| Repository | Type | Visibility | Description |
|------------|------|------------|-------------|
"""

    # Sort repositories by type, then by name
    sorted_repos = sorted(data["repositories"], key=lambda x: (x.get("type", "other"), x["name"]))

    # Add each repository as a table row
    for repo in sorted_repos:
        name = repo["name"]
        repo_type = repo.get("type", "other")
        visibility = repo.get("visibility", "unknown")
        description = repo.get("description", "No description")

        # Create visibility badge
        if visibility == "public":
            badge = "Public"
        elif visibility == "private":
            badge = "Private"
        else:
            badge = "Unknown"

        # Create type badge
        type_badges = {
            "data": "Data",
            "analysis": "Analysis",
            "metadata": "Metadata",
            "main": "Main",
            "management": "Management",
        }
        type_badge = type_badges.get(repo_type, "📁 Other")

        # Add table row with linked repository name
        content += f"| [{name}](https://github.com/{org}/{name}) | {type_badge} | {badge} | {description} |\n"

    # Add footer
    content += """
---

This catalog is automatically generated.
"""

    # Save to index.md (for GitHub Pages)
    output_path = config_dir / "index.md"
    with output_path.open("w") as f:
        f.write(content)

    print(f"Generated {output_path}")
