import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the icons inside dropdown menus
content = re.sub(r'\s*<span class="material-symbols-outlined text-\[20px\]">.*?</span>', '', content)

# Change the sidebar width
content = content.replace('"sidebar-width": "260px"', '"sidebar-width": "220px"')
content = content.replace('width: 260px;', 'width: 220px;')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
