# update_gitignore.py
content = """__pycache__/
*.pyc
.env
credentials.json
*.pdf
test_*.py
check_*.py
create_*.py
"""
with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(content)
print(".gitignore 更新完了")
