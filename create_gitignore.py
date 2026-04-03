# create_gitignore.py
content = """__pycache__/
*.pyc
.env
"""
with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(content)
print(".gitignore 作成完了")
