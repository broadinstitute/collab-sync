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
   - Go to Settings → Secrets and variables → Actions
   - Add `ADMIN_PAT`: GitHub Personal Access Token with `repo` scope

3. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from branch
   - Branch: main, folder: / (root)
   - Save

4. **Customize the YAML files**:
   - Edit `collaborators.yaml` with your actual users and repositories
   - Edit `repositories.yaml` with your actual repository information

5. **Update this README**:
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