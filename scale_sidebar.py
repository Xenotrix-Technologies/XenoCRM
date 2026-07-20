import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Separate the sidebar content to only apply replacements there
aside_start = content.find('<aside')
aside_end = content.find('</aside>') + len('</aside>')

if aside_start != -1 and aside_end != -1:
    before_aside = content[:aside_start]
    aside_content = content[aside_start:aside_end]
    after_aside = content[aside_end:]

    # Make things smaller in aside_content
    # 1. padding py-2 -> py-1.5
    aside_content = aside_content.replace('py-2', 'py-1.5')
    # 2. padding px-3 -> px-2.5
    aside_content = aside_content.replace('px-3', 'px-2.5')
    # 3. gap-3 -> gap-2
    aside_content = aside_content.replace('gap-3', 'gap-2')
    # 4. text-sm and text-body-sm -> text-[13px]
    aside_content = aside_content.replace('text-sm', 'text-[13px]')
    aside_content = aside_content.replace('text-body-sm', 'text-[13px]')
    # 5. Icon sizes -> text-[20px] for all material icons in sidebar
    # We can just change text-[20px] to text-[18px] for the ones that have it,
    # and add text-[18px] to others.
    # The default size of Material Symbols is 24px. To make them smaller, we use text-[20px] or text-[18px].
    # Let's replace 'class="material-symbols-outlined"' with 'class="material-symbols-outlined text-[20px]"'
    # but carefully avoid duplicating if it already has text-[
    aside_content = re.sub(r'class="material-symbols-outlined(?! text-\[)', r'class="material-symbols-outlined text-[20px]', aside_content)

    # Let's also reduce the font-body-sm to text-[13px] in font-body-sm
    aside_content = aside_content.replace('font-body-sm', 'text-[13px] font-body-sm')

    content = before_aside + aside_content + after_aside

# Change the sidebar width in the config and style
content = content.replace('"sidebar-width": "220px"', '"sidebar-width": "190px"')
content = content.replace('width: 220px;', 'width: 190px;')

# Change the sidebar collapsed width from 72px to 64px to make the icons more compact
content = content.replace('"sidebar-collapsed": "72px"', '"sidebar-collapsed": "64px"')
content = content.replace('width: 72px;', 'width: 64px;')
content = content.replace('margin-left: 72px;', 'margin-left: 64px;')
content = content.replace('calc(100% - 72px);', 'calc(100% - 64px);')

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
