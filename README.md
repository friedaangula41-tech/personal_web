# personal_web

Personal portfolio website built with Flet.

## Local development

```powershell
python -m pip install -r requirements.txt
python main.py
```

## GitHub Pages deployment

This repository is configured to build a static Flet site and deploy it through GitHub Actions from the `main` branch.

After pushing the workflow in [`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml), make sure the repository's Pages source is set to `GitHub Actions` in GitHub Settings.

The published site will use the repository name as its base path, so it will work under a project URL like `https://<owner>.github.io/personal_web/`.
