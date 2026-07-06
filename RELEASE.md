# Release: v1.0.0 — Initial Portfolio

Release notes and instructions for publishing the portfolio release.

Files included
- `Projects.zip` — archive of all projects and demo assets.

Suggested release notes
```
Initial portfolio snapshot: added 15 portfolio projects and 5 real-time demos.
- READMEs and usage instructions
- Demo screenshots and animated GIFs
- Sample output files
```

How to publish the release (web UI)
1. Go to the repository Releases page: https://github.com/lathadevops3/Hemalatha-Freelancing/releases
2. Click "Draft a new release".
3. Tag version: `v1.0.0`.
4. Title: "v1.0.0 — Initial Portfolio".
5. Paste the suggested release notes and upload `Projects.zip` as a release asset.
6. Publish release.

How to publish the release (GitHub CLI)
```
gh release create v1.0.0 Projects.zip --title "v1.0.0 — Initial Portfolio" --notes-file RELEASE.md
```
