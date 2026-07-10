import re
with open('templates/lead_statuses.html','r',encoding='utf-8') as f:
    content = f.read()

print("Panels:")
for m in re.finditer(r'<div id="category-panel-(.*?)"', content):
    print(m.group(1))

print("\nForms:")
for m in re.finditer(r'<form.*?id="(.*?)"', content):
    print(m.group(1))
