with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Change the sidebar width from 190px to 215px to fit the full text
content = content.replace('"sidebar-width": "190px"', '"sidebar-width": "220px"')
content = content.replace('width: 190px;', 'width: 220px;')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
