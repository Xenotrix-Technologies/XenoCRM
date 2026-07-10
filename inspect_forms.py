import re
with open('templates/lead_statuses.html','r',encoding='utf-8') as f:
    content = f.read()

print("Forms:")
for m in re.finditer(r'<form.*?id="(.*?)".*?>', content):
    print(m.group(1))

# Find the div that contains dynamic-add-status-form
idx = content.find('dynamic-add-status-form')
print("Surrounding content:")
print(content[max(0, idx-100):idx+500])
