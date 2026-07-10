import re

with open('templates/lead_statuses.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace switchCategoryTab logic
content = re.sub(r'function switchCategoryTab\(cat\) \{.*?\}\n', '', content, flags=re.DOTALL)

# In DOMContentLoaded, remove switchCategoryTab(tab)
content = re.sub(r'const urlParams = new URLSearchParams.*?switchCategoryTab\(tab\);', '', content, flags=re.DOTALL)

# Inject currentCategory
content = content.replace("let currentCategory = 'leads';", "let currentCategory = '{{ request.GET.tab|default:\"leads\" }}';")

# Also, there's no longer any need for `hidden` class on the panels or forms!
# The {% if %} handles it.
content = content.replace('class="category-panel space-y-6 hidden"', 'class="category-panel space-y-6"')
content = content.replace('class="category-panel space-y-3 hidden"', 'class="category-panel space-y-3"')
content = content.replace('class="category-form space-y-4 hidden"', 'class="category-form space-y-4"')

# Remove any remaining `.classList.remove('hidden')` just in case?
# It's fine to leave them if they don't error, but let's just make sure.

with open('templates/lead_statuses.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS refactored successfully")
