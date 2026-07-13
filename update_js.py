import re
with open('templates/role_permissions.html', 'r') as f:
    content = f.read()

new_pages = [
    'hr_dashboard', 'hr_employees', 'hr_attendance', 'hr_leaves', 'hr_payroll', 'hr_settings',
    'finance_dashboard', 'finance_income', 'finance_expenses', 'finance_reports', 'partner_payouts', 'finance_settings',
    'editor_dashboard', 'editor_board', 'post_management', 'campaign_status_settings'
]

# Find the 'const pages = [...];' line
pages_pattern = r'const pages = \[(.*?)\];'
match = re.search(pages_pattern, content)
if match:
    existing_pages = match.group(1)
    new_pages_str = ', '.join(["'" + p + "'" for p in new_pages])
    updated_pages = existing_pages + ', ' + new_pages_str
    
    content = content.replace(match.group(0), f'const pages = [{updated_pages}];')

with open('templates/role_permissions.html', 'w') as f:
    f.write(content)
print('Updated pages array in JS')
