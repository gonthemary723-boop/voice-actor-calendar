# update_workflow.py
import os

os.makedirs(".github/workflows", exist_ok=True)

content = """name: Update Calendar

on:
  schedule:
    - cron: '0 15 * * *'
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Scrape events
        run: python scraper.py

      - name: Generate ICS
        run: python generate_ics.py

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/
          git diff --staged --quiet || git commit -m "Update calendar $(date -u +%Y-%m-%d)"
          git push

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './data'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""

with open(".github/workflows/update_calendar.yml", "w", encoding="utf-8") as f:
    f.write(content)
print("ワークフロー更新完了")
