import re

with open('templates/role_permissions.html', 'r') as f:
    content = f.read()

start_idx = content.find('<!-- Row: Departments -->')
end_idx = content.find('<!-- Save Button -->')

if start_idx != -1 and end_idx != -1:
    before = content[:start_idx]
    after = content[end_idx:]

    def make_row(page_id, title, desc, icon):
        return f'''
            <!-- Row: {title} -->
            <div class="flex items-center justify-between p-4 rounded-xl border border-outline-variant/20 bg-slate-50/30 hover:bg-slate-50 transition-colors">
              <div class="flex items-center gap-3.5">
                <div class="w-10 h-10 rounded-lg bg-primary-container/10 flex items-center justify-center text-primary">
                  <span class="material-symbols-outlined text-[20px]">{icon}</span>
                </div>
                <div>
                  <span class="block text-sm font-bold text-on-surface">{title}</span>
                  <span class="block text-[11px] text-secondary">{desc}</span>
                </div>
              </div>
              <div class="flex items-center gap-4">
                <input type="checkbox" id="perm-{page_id}" class="perm-switch perm-toggle-view w-9 h-5 bg-surface-variant rounded-full appearance-none cursor-pointer relative checked:bg-primary transition-all duration-300 before:content-[''] before:absolute before:w-4 before:h-4 before:rounded-full before:bg-white before:top-0.5 before:left-0.5 checked:before:left-4.5 before:transition-all before:duration-300 shadow-inner border border-outline-variant" />
                <input type="checkbox" id="perm-{page_id}-edit" class="perm-switch-edit perm-toggle-edit w-9 h-5 bg-surface-variant rounded-full appearance-none cursor-pointer relative checked:bg-primary transition-all duration-300 before:content-[''] before:absolute before:w-4 before:h-4 before:rounded-full before:bg-white before:top-0.5 before:left-0.5 checked:before:left-4.5 before:transition-all before:duration-300 shadow-inner border border-outline-variant" />
                <input type="checkbox" id="perm-{page_id}-delete" class="perm-switch-delete perm-toggle-delete w-9 h-5 bg-surface-variant rounded-full appearance-none cursor-pointer relative checked:bg-error transition-all duration-300 before:content-[''] before:absolute before:w-4 before:h-4 before:rounded-full before:bg-white before:top-0.5 before:left-0.5 checked:before:left-4.5 before:transition-all before:duration-300 shadow-inner border border-outline-variant" />
              </div>
            </div>'''

    def make_header(title):
        return f'''
            <div class="pt-4 pb-1">
              <h4 class="text-xs font-bold uppercase tracking-wider text-outline">{title}</h4>
            </div>'''

    new_html = ""
    new_html += make_row("departments", "Departments", "Manage departments and staff assignments.", "corporate_fare")

    new_html += make_header("Human Resources")
    new_html += make_row("hr_dashboard", "HR Dashboard", "Access to HR statistics and overview.", "dashboard")
    new_html += make_row("hr_employees", "Employees", "Manage organization employees.", "badge")
    new_html += make_row("hr_attendance", "Attendance", "Manage staff attendance records.", "event_available")
    new_html += make_row("hr_leaves", "Leaves", "Manage time off requests.", "sick")
    new_html += make_row("hr_payroll", "Payroll", "Manage salaries and payroll records.", "payments")
    new_html += make_row("hr_settings", "HR Settings", "Configure HR module settings.", "settings")

    new_html += make_header("Finance")
    new_html += make_row("finance_dashboard", "Finance Dashboard", "Access to finance statistics.", "speed")
    new_html += make_row("finance_income", "Income", "Manage revenue and income streams.", "trending_up")
    new_html += make_row("finance_expenses", "Expenses", "Manage organizational expenses.", "trending_down")
    new_html += make_row("finance_reports", "Financial Reports", "Generate and view financial reports.", "assessment")
    new_html += make_row("partner_payouts", "Partner Payouts", "Manage affiliate and partner payouts.", "payments")
    new_html += make_row("finance_settings", "Finance Settings", "Configure financial settings.", "settings")

    new_html += make_header("CMS & Campaigns Subpages")
    new_html += make_row("editor_dashboard", "Editor Dashboard", "Access editor statistics.", "analytics")
    new_html += make_row("editor_board", "Editor Board", "Access content production kanban.", "edit_square")
    new_html += make_row("post_management", "Post Management", "Manage social media posts.", "campaign")
    new_html += make_row("campaign_status_settings", "Campaign Settings", "Configure campaign statuses.", "settings")

    new_html += '\n          </div>\n\n          '

    with open('templates/role_permissions.html', 'w') as f:
        f.write(before + new_html + after)

    print('Fixed layout in role_permissions.html')
