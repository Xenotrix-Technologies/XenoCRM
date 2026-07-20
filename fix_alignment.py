import re

# Update hr_settings.html
with open('templates/hr_settings.html', 'r', encoding='utf-8') as f:
    hr_content = f.read()

# Change grid layout to a max of 3 columns to give cards more breathing room
hr_content = hr_content.replace('xl:grid-cols-4', '')

# To make headers align perfectly even if they get tight, we can:
# 1. Reduce the gap from gap-3 to gap-2 in the left div.
# 2. Use flex-wrap if we really want to, or just let it wrap gracefully.
# But removing xl:grid-cols-4 will likely solve the wrapping issue entirely.
# Let's also ensure the h3 has min-w-0 if we wanted to truncate, but wrapping is okay if there's enough room.
# Actually, let's just make the left section shrink properly and the right section not shrink.
# right section: flex items-center gap-2 shrink-0
hr_content = hr_content.replace('<div class="flex items-center gap-2">', '<div class="flex items-center gap-2 shrink-0">')
hr_content = hr_content.replace('<div class="flex items-center gap-3">', '<div class="flex items-center gap-2">')
hr_content = hr_content.replace('<h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">', '<h3 class="font-bold text-sm tracking-widest text-on-surface uppercase leading-tight">')

with open('templates/hr_settings.html', 'w', encoding='utf-8') as f:
    f.write(hr_content)

# Update finance_settings.html
with open('templates/finance_settings.html', 'r', encoding='utf-8') as f:
    fin_content = f.read()

fin_content = fin_content.replace('<div class="flex items-center gap-2">', '<div class="flex items-center gap-2 shrink-0">')
fin_content = fin_content.replace('<div class="flex items-center gap-3">', '<div class="flex items-center gap-2">')
fin_content = fin_content.replace('<h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">', '<h3 class="font-bold text-sm tracking-widest text-on-surface uppercase leading-tight">')

with open('templates/finance_settings.html', 'w', encoding='utf-8') as f:
    f.write(fin_content)
