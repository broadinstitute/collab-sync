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

    # Split into existing and planned
    existing_repos = [r for r in data["repositories"] if r.get("status") != "planned"]
    planned_repos = [r for r in data["repositories"] if r.get("status") == "planned"]

    # Sort each group by type, then name
    existing_repos.sort(key=lambda x: (x.get("type", "other"), x["name"]))
    planned_repos.sort(key=lambda x: (x.get("paper") or "zzz", x["name"]))

    # Existing repos table (with GitHub links)
    for repo in existing_repos:
        name = repo["name"]
        repo_type = repo.get("type", "other")
        visibility = repo.get("visibility", "unknown")
        description = repo.get("description", "No description")
        content += f"| [{name}](https://github.com/{org}/{name}) | {repo_type} | {visibility} | {description} |\n"

    # Planned repos table (no links, show paper ID)
    if planned_repos:
        content += "\n## Planned Repositories\n\n"
        content += "| Repository | Paper | Type | Description |\n"
        content += "|------------|-------|------|-------------|\n"
        for repo in planned_repos:
            name = repo["name"]
            paper = repo.get("paper", "")
            repo_type = repo.get("type", "other")
            description = repo.get("description", "No description")
            content += f"| {name} | {paper} | {repo_type} | {description} |\n"

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
