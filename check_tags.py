import re
with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

tags = re.findall(r'{%\s*(if|elif|else|endif|with|endwith)\b.*?[%}]}', content)
print("TAGS:")
for i, tag in enumerate(tags):
    print(f"{i}: {tag}")
