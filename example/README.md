# [YOUR CONSORTIUM NAME] Collaborator Management

Manages collaborator access for [YOUR CONSORTIUM NAME] repositories using [collab-sync](https://github.com/broadinstitute/collab-sync).

## Repository Catalog

View at: https://[YOUR-ORG].github.io/[YOUR-REPO-NAME]/

---

## 🚀 SETUP INSTRUCTIONS - DELETE THIS SECTION AFTER SETUP

### Initial Setup Steps

1. **Update organization name** in both YAML files:
   - In `collaborators.yaml`: Change `YOUR-ORG-NAME` to your GitHub organization
   - In `repositories.yaml`: Change `YOUR-ORG-NAME` to your GitHub organization

2. **Add required secrets** to your repository:

   **Option A: Using GitHub Web Interface**
   - Go to Settings → Secrets and variables → Actions
   - Add `ADMIN_PAT`: GitHub Personal Access Token with `repo` scope

   **Option B: Using GitHub CLI**
   ```bash
   gh secret set ADMIN_PAT --repo YOUR-ORG-NAME/YOUR-REPO-NAME
   ```

3. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from branch
   - Branch: gh-pages, folder: / (root)
   - Save

4. **Customize the YAML files**:
   - Edit `collaborators.yaml` with your actual users and repositories
   - Edit `repositories.yaml` with your actual repository information

5. **Note about workflow files**:
   - The `.github/workflows/` directory contains GitHub Actions workflows
   - Do NOT modify the `collab-sync` URLs in the workflows - they should always point to `git+https://github.com/broadinstitute/collab-sync.git`
   - These workflows will automatically fetch and run the latest version of the tool

6. **Update this README**:
   - Replace `[YOUR CONSORTIUM NAME]` with your consortium name
   - Replace `[YOUR-ORG]` with your GitHub organization
   - Replace `[YOUR-REPO-NAME]` with this repository name
   - Delete this entire setup section

### How It Works

- When you push changes to any YAML file, the sync workflow automatically runs
- The catalog updates weekly or when you modify `repositories.yaml`
- Only manages direct collaborators (not team members)
- `collaborators.yaml` overrides manual GitHub changes

### ⬆️ DELETE EVERYTHING ABOVE THIS LINE AFTER SETUP ⬆️

---

<!-- Template sections below — fill in and remove HTML comments after setup -->

## Request Access

<!-- Describe how new collaborators request access (e.g., a Google Form, an issue template, or an email address). -->

## Repositories

Browse the full catalog at: https://[YOUR-ORG].github.io/[YOUR-REPO-NAME]/

<!-- The catalog is auto-generated from repositories.yaml. Add a brief description of the repository categories your consortium uses. -->

## Contributing

<!-- Describe how contributors can find and pick up tasks (e.g., a project board, issue labels). -->

## How This Repo Works

This repo uses [collab-sync](https://github.com/broadinstitute/collab-sync) to manage GitHub collaborator access declaratively. See [How It Works](https://github.com/broadinstitute/collab-sync#how-it-works) for the authority model and sync directions.

Two GitHub Actions workflows keep everything in sync:

- **Sync Collaborators** — runs on every push to a YAML file; applies permission changes to GitHub
- **Update Catalog** — runs weekly (and on push to `repositories.yaml`); syncs repo visibility from GitHub and deploys the catalog to GitHub Pages