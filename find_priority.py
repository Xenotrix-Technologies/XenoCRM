content=open('templates/lead_statuses.html','r',encoding='utf-8').read()
idx = content.find('id="priority-add-card"')
print(content[idx:idx+1500])
