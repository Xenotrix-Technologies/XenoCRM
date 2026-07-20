import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Separate the sidebar content
aside_start = content.find('<aside')
aside_end = content.find('</aside>') + len('</aside>')

if aside_start != -1 and aside_end != -1:
    before_aside = content[:aside_start]
    aside_content = content[aside_start:aside_end]
    after_aside = content[aside_end:]

    # Add w-full to all <a> tags that don't have it
    aside_content = re.sub(r'<a class="flex items-center', r'<a class="w-full flex items-center', aside_content)

    # To ensure text doesn't push the arrows to the right and everything aligns perfectly:
    # 1. For buttons with a dropdown, make the left div take remaining space and truncate text
    # The structure is:
    # <div class="flex items-center gap-2">
    #     <span class="material-symbols-outlined...">icon</span>
    #     <span class="...">text</span>
    # </div>
    # We will change the div to: <div class="flex items-center gap-2 flex-1 overflow-hidden">
    # And the text span to include "truncate"
    
    # We only want to do this for the divs inside the buttons/links in the sidebar.
    aside_content = aside_content.replace('<div class="flex items-center gap-2">', '<div class="flex items-center gap-2 flex-1 overflow-hidden">')
    
    # Add truncate to all the text spans inside the nav
    # The text spans look like <span class="text-[13px] font-body-sm text-[13px]">Leads</span>
    aside_content = re.sub(r'<span class="(text-\[13px\] font-body-sm text-\[13px\])">(.*?)</span>', r'<span class="\1 truncate">\2</span>', aside_content)
    
    # In some places we might just have <span class="text-[13px]">Overview</span>
    aside_content = re.sub(r'<span class="(text-\[13px\])">(.*?)</span>', r'<span class="\1 truncate">\2</span>', aside_content)

    content = before_aside + aside_content + after_aside

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
