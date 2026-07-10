import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace toggle functions with one generic function
toggle_funcs = r'''        function toggleCampaignsDropdown\(\) \{[\s\S]*?\}

        function toggleContentDropdown\(\) \{[\s\S]*?\}

        function toggleFinanceDropdown\(\) \{[\s\S]*?\}

        function toggleSettingsDropdown\(\) \{[\s\S]*?\}'''

generic_toggle = '''        function toggleSidebarDropdown(id) {
            const menu = document.getElementById(id + '-dropdown-menu');
            const btn = document.getElementById(id + '-dropdown-btn');
            const arrow = document.getElementById(id + '-arrow');
            if (!menu || !btn || !arrow) return;
            const isExpanded = btn.getAttribute('aria-expanded') === 'true';
            
            if (isExpanded) {
                menu.classList.add('hidden');
                btn.setAttribute('aria-expanded', 'false');
                arrow.style.transform = '';
            } else {
                menu.classList.remove('hidden');
                btn.setAttribute('aria-expanded', 'true');
                arrow.style.transform = 'rotate(180deg)';
            }
        }'''
content = re.sub(toggle_funcs, generic_toggle, content)

# 2. Update existing toggle dropdown calls
content = content.replace('onclick="toggleCampaignsDropdown()"', 'onclick="toggleSidebarDropdown(\'campaigns\')"')
content = content.replace('onclick="toggleContentDropdown()"', 'onclick="toggleSidebarDropdown(\'content\')"')
content = content.replace('onclick="toggleFinanceDropdown()"', 'onclick="toggleSidebarDropdown(\'finance\')"')
content = content.replace('onclick="toggleSettingsDropdown()"', 'onclick="toggleSidebarDropdown(\'settings\')"')

# 3. Add Status Settings to Campaigns dropdown
campaigns_menu_end = r'''(                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm \{% if request\.resolver_match\.url_name == 'post_management' %\}[\s\S]*?</a>\n)                </div>'''
campaigns_status = r'''\1                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'campaigns' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=campaigns">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Status Settings</span>
                    </a>
                </div>'''
content = re.sub(campaigns_menu_end, campaigns_status, content)

# 4. Add Status Settings to Finance dropdown
finance_menu_end = r'''(                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm \{% if request\.resolver_match\.url_name == 'partner_payouts' %\}[\s\S]*?</a>\n)                </div>'''
finance_status = r'''\1                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'finance' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=finance">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Status Settings</span>
                    </a>
                </div>'''
content = re.sub(finance_menu_end, finance_status, content)

# 5. Convert Leads to dropdown
leads_link = r'''            <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors \{% if request\.resolver_match\.url_name == 'leads' %\}text-primary dark:text-primary-fixed font-bold border-l-4 border-primary dark:border-primary-fixed bg-primary-container/10\{% else %\}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50\{% endif %\}" href="\{% url 'leads' %\}">\n                <span class="material-symbols-outlined">leaderboard</span>\n                <span class="font-body-sm text-body-sm">Leads</span>\n            </a>'''
leads_dropdown = '''            <!-- Leads Dropdown Accordion -->
            <div class="space-y-1">
                <button type="button" aria-expanded="false" aria-controls="leads-dropdown-menu" id="leads-dropdown-btn"
                    onclick="toggleSidebarDropdown('leads')"
                    class="w-full flex items-center justify-between px-3 py-2 rounded-lg transition-all {% if request.resolver_match.url_name == 'leads' or (request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'leads') %}text-primary dark:text-primary-fixed font-bold bg-primary-container/5{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50{% endif %}">
                    <div class="flex items-center gap-3">
                        <span class="material-symbols-outlined">leaderboard</span>
                        <span class="font-body-sm text-body-sm">Leads</span>
                    </div>
                    <span id="leads-arrow" class="material-symbols-outlined text-[16px] transition-transform duration-200">expand_more</span>
                </button>
                <div id="leads-dropdown-menu" class="pl-8 space-y-1 hidden transition-all duration-200" role="region" aria-labelledby="leads-dropdown-btn">
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'leads' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'leads' %}">
                        <span class="material-symbols-outlined text-[20px]">list</span>
                        <span>Overview</span>
                    </a>
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'leads' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=leads">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Status Settings</span>
                    </a>
                </div>
            </div>'''
content = re.sub(leads_link, leads_dropdown, content)

# 6. Convert Calendar to dropdown
calendar_link = r'''            <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors \{% if request\.resolver_match\.url_name == 'calendar' %\}text-primary dark:text-primary-fixed font-bold border-l-4 border-primary dark:border-primary-fixed bg-primary-container/10\{% else %\}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50\{% endif %\}" href="\{% url 'calendar' %\}">\n                <span class="material-symbols-outlined">event</span>\n                <span class="font-body-sm text-body-sm">Calendar</span>\n            </a>'''
calendar_dropdown = '''            <!-- Calendar Dropdown Accordion -->
            <div class="space-y-1">
                <button type="button" aria-expanded="false" aria-controls="calendar-dropdown-menu" id="calendar-dropdown-btn"
                    onclick="toggleSidebarDropdown('calendar')"
                    class="w-full flex items-center justify-between px-3 py-2 rounded-lg transition-all {% if request.resolver_match.url_name == 'calendar' or (request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'calendar') %}text-primary dark:text-primary-fixed font-bold bg-primary-container/5{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50{% endif %}">
                    <div class="flex items-center gap-3">
                        <span class="material-symbols-outlined">event</span>
                        <span class="font-body-sm text-body-sm">Calendar</span>
                    </div>
                    <span id="calendar-arrow" class="material-symbols-outlined text-[16px] transition-transform duration-200">expand_more</span>
                </button>
                <div id="calendar-dropdown-menu" class="pl-8 space-y-1 hidden transition-all duration-200" role="region" aria-labelledby="calendar-dropdown-btn">
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'calendar' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'calendar' %}">
                        <span class="material-symbols-outlined text-[20px]">event</span>
                        <span>Overview</span>
                    </a>
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'calendar' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=calendar">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Status Settings</span>
                    </a>
                </div>
            </div>'''
content = re.sub(calendar_link, calendar_dropdown, content)

# 7. Convert Clients to dropdown
clients_link = r'''            <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors \{% if request\.resolver_match\.url_name == 'clients' %\}text-primary dark:text-primary-fixed font-bold border-l-4 border-primary dark:border-primary-fixed bg-primary-container/10\{% else %\}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50\{% endif %\}" href="\{% url 'clients' %\}">\n                <span class="material-symbols-outlined">people</span>\n                <span class="font-body-sm text-body-sm">Clients</span>\n            </a>'''
clients_dropdown = '''            <!-- Clients Dropdown Accordion -->
            <div class="space-y-1">
                <button type="button" aria-expanded="false" aria-controls="clients-dropdown-menu" id="clients-dropdown-btn"
                    onclick="toggleSidebarDropdown('clients')"
                    class="w-full flex items-center justify-between px-3 py-2 rounded-lg transition-all {% if request.resolver_match.url_name == 'clients' or (request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'clients') %}text-primary dark:text-primary-fixed font-bold bg-primary-container/5{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50{% endif %}">
                    <div class="flex items-center gap-3">
                        <span class="material-symbols-outlined">people</span>
                        <span class="font-body-sm text-body-sm">Clients</span>
                    </div>
                    <span id="clients-arrow" class="material-symbols-outlined text-[16px] transition-transform duration-200">expand_more</span>
                </button>
                <div id="clients-dropdown-menu" class="pl-8 space-y-1 hidden transition-all duration-200" role="region" aria-labelledby="clients-dropdown-btn">
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'clients' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'clients' %}">
                        <span class="material-symbols-outlined text-[20px]">people</span>
                        <span>Overview</span>
                    </a>
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'clients' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=clients">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Status Settings</span>
                    </a>
                </div>
            </div>'''
content = re.sub(clients_link, clients_dropdown, content)

# 8. Convert Support to dropdown
support_link = r'''            <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors \{% if request\.resolver_match\.url_name == 'customer_support' %\}text-primary dark:text-primary-fixed font-bold border-l-4 border-primary dark:border-primary-fixed bg-primary-container/10\{% else %\}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50\{% endif %\}" href="\{% url 'customer_support' %\}">\n                <span class="material-symbols-outlined">support_agent</span>\n                <span class="font-body-sm text-body-sm">Customer Support</span>\n            </a>'''
support_dropdown = '''            <!-- Support Dropdown Accordion -->
            <div class="space-y-1">
                <button type="button" aria-expanded="false" aria-controls="support-dropdown-menu" id="support-dropdown-btn"
                    onclick="toggleSidebarDropdown('support')"
                    class="w-full flex items-center justify-between px-3 py-2 rounded-lg transition-all {% if request.resolver_match.url_name == 'customer_support' or (request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'tickets') %}text-primary dark:text-primary-fixed font-bold bg-primary-container/5{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50{% endif %}">
                    <div class="flex items-center gap-3">
                        <span class="material-symbols-outlined">support_agent</span>
                        <span class="font-body-sm text-body-sm">Customer Support</span>
                    </div>
                    <span id="support-arrow" class="material-symbols-outlined text-[16px] transition-transform duration-200">expand_more</span>
                </button>
                <div id="support-dropdown-menu" class="pl-8 space-y-1 hidden transition-all duration-200" role="region" aria-labelledby="support-dropdown-btn">
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'customer_support' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'customer_support' %}">
                        <span class="material-symbols-outlined text-[20px]">support_agent</span>
                        <span>Overview</span>
                    </a>
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'tickets' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=tickets">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Ticket Status</span>
                    </a>
                </div>
            </div>'''
content = re.sub(support_link, support_dropdown, content)

# 9. Convert Projects to dropdown
projects_link = r'''            <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors \{% if request\.resolver_match\.url_name == 'projects' %\}text-primary dark:text-primary-fixed font-bold border-l-4 border-primary dark:border-primary-fixed bg-primary-container/10\{% else %\}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50\{% endif %\}" href="\{% url 'projects' %\}">\n                <span class="material-symbols-outlined">assignment</span>\n                <span class="font-body-sm text-body-sm">Projects</span>\n            </a>'''
projects_dropdown = '''            <!-- Projects Dropdown Accordion -->
            <div class="space-y-1">
                <button type="button" aria-expanded="false" aria-controls="projects-dropdown-menu" id="projects-dropdown-btn"
                    onclick="toggleSidebarDropdown('projects')"
                    class="w-full flex items-center justify-between px-3 py-2 rounded-lg transition-all {% if request.resolver_match.url_name == 'projects' or (request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'projects') %}text-primary dark:text-primary-fixed font-bold bg-primary-container/5{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/50{% endif %}">
                    <div class="flex items-center gap-3">
                        <span class="material-symbols-outlined">assignment</span>
                        <span class="font-body-sm text-body-sm">Projects</span>
                    </div>
                    <span id="projects-arrow" class="material-symbols-outlined text-[16px] transition-transform duration-200">expand_more</span>
                </button>
                <div id="projects-dropdown-menu" class="pl-8 space-y-1 hidden transition-all duration-200" role="region" aria-labelledby="projects-dropdown-btn">
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'projects' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'projects' %}">
                        <span class="material-symbols-outlined text-[20px]">assignment</span>
                        <span>Overview</span>
                    </a>
                    <a class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm {% if request.resolver_match.url_name == 'status_settings' and request.GET.tab == 'projects' %}text-primary dark:text-primary-fixed font-bold bg-primary-container/10{% else %}text-secondary dark:text-secondary-fixed-dim hover:bg-surface-variant/30{% endif %}" href="{% url 'status_settings' %}?tab=projects">
                        <span class="material-symbols-outlined text-[20px]">settings</span>
                        <span>Status Settings</span>
                    </a>
                </div>
            </div>'''
content = re.sub(projects_link, projects_dropdown, content)

# 10. Update Active Dropdown code on DOMContentLoaded
active_js = r'''                const btn = menu\.previousElementSibling;
                if \(btn\) \{
                    btn\.setAttribute\('aria-expanded', 'true'\);
                    const arrow = btn\.querySelector\('\.transition-transform'\);
                    if \(arrow\) arrow\.style\.transform = 'rotate\(180deg\)';
                \}'''

active_js_replacement = '''                const btn = menu.previousElementSibling;
                if (btn) {
                    btn.setAttribute('aria-expanded', 'true');
                    const arrow = btn.querySelector('.transition-transform');
                    if (arrow) arrow.style.transform = 'rotate(180deg)';
                }
            });
            
            // Auto expand for status settings active tabs
            const urlParams = new URLSearchParams(window.location.search);
            if (window.location.pathname.includes('/statuses/')) {
                const tab = urlParams.get('tab') || 'leads';
                let dropdownId = null;
                if (tab === 'leads') dropdownId = 'leads';
                if (tab === 'clients') dropdownId = 'clients';
                if (tab === 'projects') dropdownId = 'projects';
                if (tab === 'campaigns') dropdownId = 'campaigns';
                if (tab === 'calendar') dropdownId = 'calendar';
                if (tab === 'tickets') dropdownId = 'support';
                if (tab === 'finance') dropdownId = 'finance';
                if (dropdownId) {
                    const menu = document.getElementById(dropdownId + '-dropdown-menu');
                    const btn = document.getElementById(dropdownId + '-dropdown-btn');
                    const arrow = document.getElementById(dropdownId + '-arrow');
                    if (menu && btn) {
                        menu.classList.remove('hidden');
                        btn.setAttribute('aria-expanded', 'true');
                        if (arrow) arrow.style.transform = 'rotate(180deg)';
                    }
                }
            }'''
content = re.sub(active_js, active_js_replacement, content, count=1)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Base refactored successfully.")
