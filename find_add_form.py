content=open('templates/lead_statuses.html','r',encoding='utf-8').read()
idx = content.find('id="add-status-form"')
print(content[max(0,idx-200):idx+50])
