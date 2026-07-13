import re
with open('templates/base.html', 'r') as f:
    content = f.read()

# 1. Wrap HR subpages
hr_pages = ['hr_dashboard', 'hr_employees', 'hr_attendance', 'hr_leaves', 'hr_payroll', 'hr_settings']
for p in hr_pages:
    pattern = r'(<a[^>]*href=\"\{\% url \'' + p + r'\' \%\}[^>]*>.*?</a>)'
    content = re.sub(pattern, r'{% if request.user.profile.has_access_' + p + r' %}\n\1\n{% endif %}', content, flags=re.DOTALL)

# 2. Finance Accordion wrapper
finance_start = r'<!-- Finance Dropdown Accordion -->'
content = content.replace(finance_start, '{% if request.user.profile.has_access_finance %}\n            ' + finance_start)
finance_end_pattern = r'(<div id=\"finance-dropdown-menu\".*?</div>\s*</div>)'
content = re.sub(finance_end_pattern, r'\1\n            {% endif %}', content, flags=re.DOTALL)

# 3. Wrap Finance subpages
finance_pages = ['finance_dashboard', 'finance_income', 'finance_expenses', 'finance_reports', 'partner_payouts', 'finance_settings']
for p in finance_pages:
    pattern = r'(<a[^>]*href=\"\{\% url \'' + p + r'\' \%\}[^>]*>.*?</a>)'
    content = re.sub(pattern, r'{% if request.user.profile.has_access_' + p + r' %}\n\1\n{% endif %}', content, flags=re.DOTALL)

# 4. Wrap Campaigns subpages
camp_pages = ['campaign', 'post_management', 'campaign_status_settings']
for p in camp_pages:
    pattern = r'(<a[^>]*href=\"\{\% url \'' + p + r'\' \%\}[^>]*>.*?</a>)'
    content = re.sub(pattern, r'{% if request.user.profile.has_access_' + p + r' %}\n\1\n{% endif %}', content, flags=re.DOTALL)

# 5. CMS wrapper
content = content.replace('{% if request.user.profile.has_access_content_tracker %}', '{% if request.user.profile.has_access_cms %}', 1)

# 6. Wrap CMS subpages
cms_pages = ['content_tracker', 'editor_dashboard', 'editor_board']
for p in cms_pages:
    pattern = r'(<a[^>]*href=\"\{\% url \'' + p + r'\' \%\}[^>]*>.*?</a>)'
    content = re.sub(pattern, r'{% if request.user.profile.has_access_' + p + r' %}\n\1\n{% endif %}', content, flags=re.DOTALL)

with open('templates/base.html', 'w') as f:
    f.write(content)
print('Done modifying base.html')
