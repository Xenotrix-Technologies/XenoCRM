import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'status_settings'", "'lead_statuses'")

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("URL names fixed.")
