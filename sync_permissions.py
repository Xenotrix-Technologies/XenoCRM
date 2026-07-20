import os

new_html = """{% extends 'base.html' %}
{% block title %}Permissions Management - XenoCRM{% endblock %}

{% block content %}
<style>
    /* Custom Toggle Switch for Table */
    .matrix-toggle {
        width: 36px;
        height: 20px;
        background-color: #e2e8f0;
        border-radius: 9999px;
        appearance: none;
        cursor: pointer;
        position: relative;
        transition: background-color 0.3s;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
        border: 1px solid #cbd5e1;
    }
    .matrix-toggle::before {
        content: '';
        position: absolute;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background-color: white;
        top: 1px;
        left: 1px;
        transition: transform 0.3s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    .matrix-toggle:checked {
        background-color: #3b82f6; /* primary blue */
        border-color: #2563eb;
    }
    .matrix-toggle:checked::before {
        transform: translateX(16px);
    }
    .matrix-toggle.toggle-delete:checked {
        background-color: #ef4444; /* red for delete */
        border-color: #dc2626;
    }
</style>

<script>
    const rolePermissionsData = {{ role_permissions_json|safe }};
    const staffPermissionsData = {{ staff_permissions_json|safe }};
</script>

<main class="pt-8 p-margin-edge min-h-screen bg-slate-50/50">
  <div class="max-w-[1400px] mx-auto">
    <!-- Breadcrumbs -->
    <div class="flex items-center gap-2 mb-6 font-label-md text-outline">
      <a href="{% url 'dashboard' %}" class="hover:underline">Dashboard</a>
      <span class="material-symbols-outlined text-[14px]">chevron_right</span>
      <span class="text-primary font-bold">Permissions Management</span>
    </div>

    <!-- 2-Column Layout -->
    <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-12 gap-6">
      
      <!-- Left Sidebar: Selection Pane (25%) -->
      <div class="md:col-span-4 lg:col-span-3 flex flex-col h-[calc(100vh-140px)]">
        <div class="bg-white rounded-[16px] shadow-sm border border-outline-variant/50 flex flex-col h-full overflow-hidden">
            
            <!-- Segmented Control -->
            <div class="p-4 border-b border-outline-variant/30 bg-slate-50/50">
                <div class="flex p-1 bg-slate-200/70 rounded-xl">
                    <button onclick="switchViewMode('role')" id="btn-mode-role" class="flex-1 py-1.5 text-xs font-bold rounded-lg transition-all bg-white shadow-sm text-primary">System Roles</button>
                    <button onclick="switchViewMode('staff')" id="btn-mode-staff" class="flex-1 py-1.5 text-xs font-bold rounded-lg transition-all text-secondary hover:text-on-surface">Employees</button>
                </div>
            </div>
            
            <div class="p-4 flex flex-col flex-1 overflow-hidden">
                <!-- Search -->
                <div class="relative mb-4">
                    <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[18px] text-outline">search</span>
                    <input type="text" id="target-search-input" onkeyup="filterTargets()" placeholder="Search..." class="w-full bg-slate-50 border border-outline-variant/50 text-sm rounded-xl pl-10 pr-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-on-surface placeholder:text-outline/70" />
                </div>

                <!-- Roles Container -->
                <div class="space-y-2 overflow-y-auto custom-scrollbar flex-1 pr-1" id="roles-container">
                    {% for role in roles %}
                    <button type="button" 
                            onclick="selectTarget('role', '{{ role.name|escapejs }}', '{{ role.name|escapejs }}', 'System Role')"
                            id="target-role-{{ role.name|slugify }}" 
                            class="target-card target-role w-full flex items-center justify-between p-4 rounded-xl border border-transparent hover:border-outline-variant/50 hover:bg-slate-50 transition-all text-left group">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-lg bg-primary/5 text-primary flex items-center justify-center group-hover:bg-primary/10 transition-colors">
                                <span class="material-symbols-outlined text-[18px]">badge</span>
                            </div>
                            <span class="font-bold text-sm text-on-surface target-name">{{ role.name }}</span>
                        </div>
                    </button>
                    {% endfor %}
                </div>

                <!-- Staff Container (Hidden by default) -->
                <div class="space-y-2 overflow-y-auto custom-scrollbar flex-1 pr-1 hidden" id="staff-container">
                    {% for staff in staff_members %}
                    <button type="button" 
                            onclick="selectTarget('staff', '{{ staff.id }}', '{{ staff.user.get_full_name|default:staff.user.username|escapejs }}', '{{ staff.role.name|default:"Employee"|escapejs }}')"
                            id="target-staff-{{ staff.id }}" 
                            class="target-card target-staff w-full flex items-center justify-between p-3 rounded-xl border border-transparent hover:border-outline-variant/50 hover:bg-slate-50 transition-all text-left group">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-secondary/10 text-secondary flex items-center justify-center group-hover:bg-primary/10 group-hover:text-primary transition-colors uppercase font-bold text-xs">
                                {{ staff.user.first_name|slice:":1" }}{{ staff.user.last_name|slice:":1" }}
                            </div>
                            <div>
                                <span class="block font-bold text-sm text-on-surface target-name">{{ staff.user.get_full_name|default:staff.user.username }}</span>
                                <span class="block text-[10px] text-outline font-semibold uppercase">{{ staff.role.name|default:"No Role" }}</span>
                            </div>
                        </div>
                    </button>
                    {% endfor %}
                </div>

                <!-- Create Button -->
                <div class="pt-4 mt-2 border-t border-outline-variant/30">
                    <a href="{% url 'add_staff_role' %}" id="create-btn" class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl border border-primary text-primary hover:bg-primary/5 font-bold text-sm transition-colors">
                        <span class="material-symbols-outlined text-[18px]">add</span>
                        <span id="create-btn-text">Create Role</span>
                    </a>
                </div>
            </div>
        </div>
      </div>

      <!-- Right Content Area: Permissions (75%) -->
      <div class="md:col-span-8 lg:col-span-9 flex flex-col h-[calc(100vh-140px)] hidden" id="permissions-pane">
        
        <div class="bg-white rounded-[16px] shadow-sm border border-outline-variant/50 flex flex-col h-full overflow-hidden relative">
            
            <!-- Header Section -->
            <div class="p-6 border-b border-outline-variant/30 bg-slate-50/50">
                <div class="flex items-start justify-between">
                    <div>
                        <div class="flex items-center gap-3 mb-1">
                            <h2 class="font-headline-md text-2xl font-bold text-on-surface" id="selected-target-name">Name</h2>
                            <span class="bg-green-100 text-green-700 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full" id="selected-target-badge1">Active</span>
                            <span class="bg-blue-100 text-blue-700 text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full" id="selected-target-badge2">System Role</span>
                        </div>
                        <p class="text-sm text-secondary" id="selected-target-desc">System access configuration for this entity.</p>
                    </div>
                    
                    <!-- Statistics Cards -->
                    <div class="flex gap-4">
                        <div class="bg-white border border-outline-variant/50 rounded-xl px-4 py-2 text-center shadow-sm">
                            <span class="block text-[10px] font-bold uppercase tracking-wider text-outline mb-0.5">Total Modules</span>
                            <span class="block font-bold text-lg text-on-surface">15</span>
                        </div>
                        <div class="bg-white border border-outline-variant/50 rounded-xl px-4 py-2 text-center shadow-sm">
                            <span class="block text-[10px] font-bold uppercase tracking-wider text-outline mb-0.5">Total Perms</span>
                            <span class="block font-bold text-lg text-on-surface">45</span>
                        </div>
                        <div class="bg-white border border-outline-variant/50 rounded-xl px-4 py-2 text-center shadow-sm">
                            <span class="block text-[10px] font-bold uppercase tracking-wider text-primary mb-0.5">Active Perms</span>
                            <span class="block font-bold text-lg text-primary" id="active-perms-count">0</span>
                        </div>
                    </div>
                </div>
                <!-- Override Alert -->
                <div id="override-alert" class="mt-4 p-3 rounded-lg bg-orange-50 border border-orange-200 flex items-start gap-3 hidden">
                    <span class="material-symbols-outlined text-orange-500">warning</span>
                    <div>
                        <span class="block text-sm font-bold text-orange-800">Employee Overrides</span>
                        <span class="block text-xs text-orange-700">These permissions will override the employee's base role permissions. Leaving them unchecked removes access.</span>
                    </div>
                </div>
            </div>

            <!-- Permission Tabs -->
            <div class="px-6 pt-4 flex gap-6 border-b border-outline-variant/30 overflow-x-auto custom-scrollbar whitespace-nowrap">
                <button onclick="filterCategory('All')" id="tab-All" class="perm-tab pb-3 text-sm font-bold text-primary border-b-2 border-primary transition-colors">All Modules</button>
                <button onclick="filterCategory('CRM')" id="tab-CRM" class="perm-tab pb-3 text-sm font-bold text-secondary hover:text-on-surface border-b-2 border-transparent transition-colors">CRM</button>
                <button onclick="filterCategory('Finance')" id="tab-Finance" class="perm-tab pb-3 text-sm font-bold text-secondary hover:text-on-surface border-b-2 border-transparent transition-colors">Finance</button>
                <button onclick="filterCategory('HR')" id="tab-HR" class="perm-tab pb-3 text-sm font-bold text-secondary hover:text-on-surface border-b-2 border-transparent transition-colors">HR</button>
                <button onclick="filterCategory('Marketing')" id="tab-Marketing" class="perm-tab pb-3 text-sm font-bold text-secondary hover:text-on-surface border-b-2 border-transparent transition-colors">Marketing</button>
                <button onclick="filterCategory('CMS')" id="tab-CMS" class="perm-tab pb-3 text-sm font-bold text-secondary hover:text-on-surface border-b-2 border-transparent transition-colors">CMS</button>
                <button onclick="filterCategory('Settings')" id="tab-Settings" class="perm-tab pb-3 text-sm font-bold text-secondary hover:text-on-surface border-b-2 border-transparent transition-colors">Settings</button>
            </div>

            <!-- Matrix Toolbar -->
            <div class="px-6 py-3 flex items-center justify-between bg-slate-50/50 border-b border-outline-variant/30">
                <div class="relative w-64">
                    <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-[16px] text-outline">search</span>
                    <input type="text" id="module-search-input" onkeyup="filterModules()" placeholder="Search modules..." class="w-full bg-white border border-outline-variant/50 text-xs rounded-lg pl-9 pr-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-on-surface" />
                </div>
            </div>

            <!-- Permission Matrix -->
            <div class="flex-1 overflow-auto custom-scrollbar relative">
                <table class="w-full text-left border-collapse" id="permission-matrix">
                    <thead class="sticky top-0 bg-slate-100 z-10 shadow-sm">
                        <tr>
                            <th class="py-3 px-6 text-xs font-bold uppercase tracking-wider text-secondary border-b border-outline-variant/30">Module</th>
                            <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider text-secondary border-b border-outline-variant/30 text-center">
                                <div class="flex flex-col items-center gap-1">
                                    <span>View</span>
                                    <input type="checkbox" onclick="toggleColumn('view', this.checked)" class="rounded text-primary focus:ring-primary w-3.5 h-3.5 cursor-pointer">
                                </div>
                            </th>
                            <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider text-secondary border-b border-outline-variant/30 text-center">
                                <div class="flex flex-col items-center gap-1">
                                    <span>Create/Edit</span>
                                    <input type="checkbox" onclick="toggleColumn('edit', this.checked)" class="rounded text-primary focus:ring-primary w-3.5 h-3.5 cursor-pointer">
                                </div>
                            </th>
                            <th class="py-3 px-4 text-xs font-bold uppercase tracking-wider text-secondary border-b border-outline-variant/30 text-center">
                                <div class="flex flex-col items-center gap-1">
                                    <span>Delete</span>
                                    <input type="checkbox" onclick="toggleColumn('delete', this.checked)" class="rounded text-primary focus:ring-primary w-3.5 h-3.5 cursor-pointer">
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody id="matrix-body" class="bg-white">
                        <!-- Module Rows -->
                        
                        <!-- CRM: Dashboard -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Dashboard">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">dashboard</span><div><span class="block text-sm font-bold text-on-surface">Dashboard</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-dashboard" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><span class="text-outline text-xs">-</span></td>
                            <td class="py-3 px-4 text-center"><span class="text-outline text-xs">-</span></td>
                        </tr>

                        <!-- CRM: Leads -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Leads">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">leaderboard</span><div><span class="block text-sm font-bold text-on-surface">Leads Pipeline</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-leads" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-leads-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-leads-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- CRM: Calendar -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Calendar">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">event</span><div><span class="block text-sm font-bold text-on-surface">Calendar</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-calendar" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-calendar-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-calendar-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- CRM: Clients -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Clients">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">people</span><div><span class="block text-sm font-bold text-on-surface">Clients Database</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-clients" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-clients-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-clients-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- CRM: Customer Support -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Customer Support">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">support_agent</span><div><span class="block text-sm font-bold text-on-surface">Customer Support</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-support" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-support-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-support-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>
                        
                        <!-- CRM: Projects -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Projects">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">assignment</span><div><span class="block text-sm font-bold text-on-surface">Projects Board</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-projects" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-projects-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-projects-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- CRM: Agreements -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CRM" data-name="Agreements">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">history_edu</span><div><span class="block text-sm font-bold text-on-surface">Agreements</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-agreements" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-agreements-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-agreements-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- HR: Staff -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="HR" data-name="Staff">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">badge</span><div><span class="block text-sm font-bold text-on-surface">Staff Directory</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-staff" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-staff-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-staff-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- HR: Human Resources -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="HR" data-name="Human Resources">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">groups</span><div><span class="block text-sm font-bold text-on-surface">Human Resources</span><span class="block text-[11px] text-secondary">Leaves, Attendance, Payroll.</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-hr" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-hr-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-hr-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- Marketing: Campaigns -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="Marketing" data-name="Campaigns">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">ads_click</span><div><span class="block text-sm font-bold text-on-surface">Campaigns</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-campaigns" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-campaigns-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-campaigns-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- CMS: Content Tracker -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="CMS" data-name="CMS">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">video_library</span><div><span class="block text-sm font-bold text-on-surface">CMS & Content Tracker</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-content_tracker" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-content_tracker-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-content_tracker-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- Finance: Finance -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="Finance" data-name="Finance">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">payments</span><div><span class="block text-sm font-bold text-on-surface">Finance</span><span class="block text-[11px] text-secondary">Income, Expenses, Partner Payouts.</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-finance" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-finance-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-finance-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- Settings -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="Settings" data-name="Settings">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">settings</span><div><span class="block text-sm font-bold text-on-surface">Settings</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-settings" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-settings-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-settings-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>

                        <!-- Role Permissions -->
                        <tr class="border-b border-outline-variant/20 hover:bg-slate-50 transition-colors matrix-row" data-category="Settings" data-name="Role Permissions">
                            <td class="py-3 px-6"><div class="flex items-center gap-3"><span class="material-symbols-outlined text-outline text-[18px]">rule</span><div><span class="block text-sm font-bold text-on-surface">Role Permissions</span></div></div></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-role_permissions" class="matrix-toggle perm-view" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-role_permissions-edit" class="matrix-toggle perm-edit" onchange="updateCount()" /></td>
                            <td class="py-3 px-4 text-center"><input type="checkbox" id="perm-role_permissions-delete" class="matrix-toggle toggle-delete perm-delete" onchange="updateCount()" /></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Action Buttons Footer -->
            <div class="px-6 py-4 bg-white border-t border-outline-variant/30 flex justify-end gap-3 z-20">
                <button type="button" class="px-4 py-2 text-sm font-bold text-secondary bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors">Clone Config</button>
                <button type="button" onclick="loadPermissionsForTarget()" class="px-4 py-2 text-sm font-bold text-error border border-error/30 hover:bg-error/5 rounded-xl transition-colors">Reset</button>
                <button type="button" onclick="savePermissions()" class="px-6 py-2 text-sm font-bold text-white bg-primary hover:bg-primary/90 shadow rounded-xl transition-all">Save Permissions</button>
            </div>
            
            <!-- Loading Overlay -->
            <div id="loading-overlay" class="absolute inset-0 bg-white/80 backdrop-blur-sm z-50 flex items-center justify-center hidden">
                <div class="flex flex-col items-center gap-3">
                    <div class="w-8 h-8 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
                    <span class="text-sm font-bold text-secondary">Saving permissions...</span>
                </div>
            </div>
        </div>
      </div>
      
    </div>
  </div>
</main>

<script>
    let currentType = 'role';
    let currentId = null;
    
    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll('.matrix-toggle').forEach(el => el.checked = false);
    });

    function switchViewMode(mode) {
        currentType = mode;
        const btnRole = document.getElementById('btn-mode-role');
        const btnStaff = document.getElementById('btn-mode-staff');
        
        if (mode === 'role') {
            btnRole.classList.replace('text-secondary', 'text-primary');
            btnRole.classList.add('bg-white', 'shadow-sm');
            btnRole.classList.remove('hover:text-on-surface');
            
            btnStaff.classList.replace('text-primary', 'text-secondary');
            btnStaff.classList.remove('bg-white', 'shadow-sm');
            btnStaff.classList.add('hover:text-on-surface');
            
            document.getElementById('roles-container').classList.remove('hidden');
            document.getElementById('staff-container').classList.add('hidden');
            
            document.getElementById('create-btn-text').innerText = "Create Role";
            document.getElementById('create-btn').href = "{% url 'add_staff_role' %}";
        } else {
            btnStaff.classList.replace('text-secondary', 'text-primary');
            btnStaff.classList.add('bg-white', 'shadow-sm');
            btnStaff.classList.remove('hover:text-on-surface');
            
            btnRole.classList.replace('text-primary', 'text-secondary');
            btnRole.classList.remove('bg-white', 'shadow-sm');
            btnRole.classList.add('hover:text-on-surface');
            
            document.getElementById('roles-container').classList.add('hidden');
            document.getElementById('staff-container').classList.remove('hidden');
            
            document.getElementById('create-btn-text').innerText = "Add Employee";
            document.getElementById('create-btn').href = "{% url 'add_staff' %}";
        }
        
        document.getElementById('permissions-pane').classList.add('hidden');
        filterTargets();
    }

    function filterTargets() {
        const query = document.getElementById('target-search-input').value.toLowerCase();
        const selector = currentType === 'role' ? '.target-role' : '.target-staff';
        document.querySelectorAll(selector).forEach(card => {
            const name = card.querySelector('.target-name').innerText.toLowerCase();
            card.style.display = name.includes(query) ? 'flex' : 'none';
        });
    }

    function selectTarget(type, id, displayName, subText) {
        currentType = type;
        currentId = id;
        
        // Update Sidebar UI
        document.querySelectorAll('.target-card').forEach(el => {
            el.classList.remove('border-primary', 'bg-primary/5');
            el.classList.add('border-transparent');
        });
        
        let tabId = type === 'role' ? `target-role-${id.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '')}` : `target-staff-${id}`;
        const activeTab = document.getElementById(tabId);
        if (activeTab) {
            activeTab.classList.remove('border-transparent');
            activeTab.classList.add('border-primary', 'bg-primary/5');
        }

        // Show permissions pane
        document.getElementById('permissions-pane').classList.remove('hidden');
        
        // Update Header
        document.getElementById('selected-target-name').innerText = displayName;
        
        if (type === 'role') {
            document.getElementById('selected-target-badge1').innerText = "Active";
            document.getElementById('selected-target-badge2').innerText = "System Role";
            document.getElementById('override-alert').classList.add('hidden');
            document.getElementById('selected-target-desc').innerText = "System access configuration for this role.";
        } else {
            document.getElementById('selected-target-badge1').innerText = "Employee";
            document.getElementById('selected-target-badge2').innerText = subText; // Base role name
            document.getElementById('override-alert').classList.remove('hidden');
            document.getElementById('selected-target-desc').innerText = "Custom override permissions for this employee.";
        }
        
        // Load permissions
        loadPermissionsForTarget();
    }

    function loadPermissionsForTarget() {
        if (!currentId) return;
        
        document.querySelectorAll('.matrix-toggle').forEach(el => el.checked = false);
        
        const p = currentType === 'role' ? (rolePermissionsData[currentId] || {}) : (staffPermissionsData[currentId] || {});
        
        // Simple mapping function
        const mapPerm = (id, val) => {
            const el = document.getElementById(id);
            if(el) el.checked = val === true;
        };
        
        mapPerm('perm-dashboard', p.can_view_dashboard);
        
        mapPerm('perm-leads', p.can_view_leads);
        mapPerm('perm-leads-edit', p.can_edit_leads);
        mapPerm('perm-leads-delete', p.can_delete_leads);
        
        mapPerm('perm-calendar', p.can_view_calendar);
        mapPerm('perm-calendar-edit', p.can_edit_calendar);
        mapPerm('perm-calendar-delete', p.can_delete_calendar);
        
        mapPerm('perm-clients', p.can_view_clients);
        mapPerm('perm-clients-edit', p.can_edit_clients);
        mapPerm('perm-clients-delete', p.can_delete_clients);
        
        mapPerm('perm-support', p.can_view_support);
        mapPerm('perm-support-edit', p.can_edit_support);
        mapPerm('perm-support-delete', p.can_delete_support);
        
        mapPerm('perm-projects', p.can_view_projects);
        mapPerm('perm-projects-edit', p.can_edit_projects);
        mapPerm('perm-projects-delete', p.can_delete_projects);
        
        mapPerm('perm-agreements', p.can_view_agreements);
        mapPerm('perm-agreements-edit', p.can_edit_agreements);
        mapPerm('perm-agreements-delete', p.can_delete_agreements);
        
        mapPerm('perm-staff', p.can_view_staff);
        mapPerm('perm-staff-edit', p.can_edit_staff);
        mapPerm('perm-staff-delete', p.can_delete_staff);

        mapPerm('perm-hr', p.can_view_hr);
        mapPerm('perm-hr-edit', p.can_edit_hr);
        mapPerm('perm-hr-delete', p.can_delete_hr);
        
        mapPerm('perm-campaigns', p.can_view_campaigns);
        mapPerm('perm-campaigns-edit', p.can_edit_campaigns);
        mapPerm('perm-campaigns-delete', p.can_delete_campaigns);
        
        mapPerm('perm-content_tracker', p.can_view_content_tracker);
        mapPerm('perm-content_tracker-edit', p.can_edit_content_tracker);
        mapPerm('perm-content_tracker-delete', p.can_delete_content_tracker);

        mapPerm('perm-finance', p.can_view_finance);
        mapPerm('perm-finance-edit', p.can_edit_finance);
        mapPerm('perm-finance-delete', p.can_delete_finance);
        
        mapPerm('perm-settings', p.can_view_settings);
        mapPerm('perm-settings-edit', p.can_edit_settings);
        mapPerm('perm-settings-delete', p.can_delete_settings);
        
        mapPerm('perm-role_permissions', p.can_view_role_permissions);
        mapPerm('perm-role_permissions-edit', p.can_edit_role_permissions);
        mapPerm('perm-role_permissions-delete', p.can_delete_role_permissions);
        
        updateCount();
    }

    function savePermissions() {
        if (!currentId) return;

        const overlay = document.getElementById('loading-overlay');
        overlay.classList.remove('hidden');

        // Collect permissions
        const getVal = id => {
            const el = document.getElementById(id);
            return el ? el.checked : false;
        };

        const payload = {
            type: currentType,
            id: currentId,
            permissions: {
                can_view_dashboard: getVal('perm-dashboard'),
                
                can_view_leads: getVal('perm-leads'),
                can_edit_leads: getVal('perm-leads-edit'),
                can_delete_leads: getVal('perm-leads-delete'),
                
                can_view_calendar: getVal('perm-calendar'),
                can_edit_calendar: getVal('perm-calendar-edit'),
                can_delete_calendar: getVal('perm-calendar-delete'),
                
                can_view_clients: getVal('perm-clients'),
                can_edit_clients: getVal('perm-clients-edit'),
                can_delete_clients: getVal('perm-clients-delete'),
                
                can_view_support: getVal('perm-support'),
                can_edit_support: getVal('perm-support-edit'),
                can_delete_support: getVal('perm-support-delete'),
                
                can_view_projects: getVal('perm-projects'),
                can_edit_projects: getVal('perm-projects-edit'),
                can_delete_projects: getVal('perm-projects-delete'),
                
                can_view_agreements: getVal('perm-agreements'),
                can_edit_agreements: getVal('perm-agreements-edit'),
                can_delete_agreements: getVal('perm-agreements-delete'),
                
                can_view_staff: getVal('perm-staff'),
                can_edit_staff: getVal('perm-staff-edit'),
                can_delete_staff: getVal('perm-staff-delete'),

                can_view_hr: getVal('perm-hr'),
                can_edit_hr: getVal('perm-hr-edit'),
                can_delete_hr: getVal('perm-hr-delete'),
                
                can_view_campaigns: getVal('perm-campaigns'),
                can_edit_campaigns: getVal('perm-campaigns-edit'),
                can_delete_campaigns: getVal('perm-campaigns-delete'),
                
                can_view_content_tracker: getVal('perm-content_tracker'),
                can_edit_content_tracker: getVal('perm-content_tracker-edit'),
                can_delete_content_tracker: getVal('perm-content_tracker-delete'),

                can_view_finance: getVal('perm-finance'),
                can_edit_finance: getVal('perm-finance-edit'),
                can_delete_finance: getVal('perm-finance-delete'),
                
                can_view_settings: getVal('perm-settings'),
                can_edit_settings: getVal('perm-settings-edit'),
                can_delete_settings: getVal('perm-settings-delete'),
                
                can_view_role_permissions: getVal('perm-role_permissions'),
                can_edit_role_permissions: getVal('perm-role_permissions-edit'),
                can_delete_role_permissions: getVal('perm-role_permissions-delete')
            }
        };

        fetch("{% url 'role_permissions' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(res => {
            overlay.classList.add('hidden');
            if(res.success) {
                // Update local data cache
                if (currentType === 'role') {
                    rolePermissionsData[currentId] = payload.permissions;
                } else {
                    staffPermissionsData[currentId] = payload.permissions;
                }
                
                // Flash success (simple feedback)
                const saveBtn = document.querySelector('button[onclick="savePermissions()"]');
                const origText = saveBtn.innerText;
                saveBtn.innerText = "Saved!";
                saveBtn.classList.add('bg-green-600');
                setTimeout(() => {
                    saveBtn.innerText = origText;
                    saveBtn.classList.remove('bg-green-600');
                }, 2000);
            } else {
                alert("Error saving: " + res.error);
            }
        })
        .catch(err => {
            overlay.classList.add('hidden');
            console.error("Save error:", err);
            alert("Error saving permissions.");
        });
    }

    function filterCategory(cat) {
        // Update tabs styling
        document.querySelectorAll('.perm-tab').forEach(el => {
            el.classList.remove('text-primary', 'border-primary');
            el.classList.add('text-secondary', 'border-transparent');
        });
        const activeTab = document.getElementById('tab-' + cat);
        activeTab.classList.remove('text-secondary', 'border-transparent');
        activeTab.classList.add('text-primary', 'border-primary');

        // Filter rows
        document.querySelectorAll('.matrix-row').forEach(row => {
            if (cat === 'All' || row.dataset.category === cat) {
                row.style.display = 'table-row';
            } else {
                row.style.display = 'none';
            }
        });
    }

    function filterModules() {
        const query = document.getElementById('module-search-input').value.toLowerCase();
        document.querySelectorAll('.matrix-row').forEach(row => {
            const name = row.dataset.name.toLowerCase();
            row.style.display = name.includes(query) ? 'table-row' : 'none';
        });
        
        // Reset tabs to All if searching
        if(query) {
            document.querySelectorAll('.perm-tab').forEach(el => {
                el.classList.remove('text-primary', 'border-primary');
                el.classList.add('text-secondary', 'border-transparent');
            });
            document.getElementById('tab-All').classList.remove('text-secondary', 'border-transparent');
            document.getElementById('tab-All').classList.add('text-primary', 'border-primary');
        }
    }

    function toggleColumn(type, checked) {
        document.querySelectorAll(`.perm-${type}`).forEach(toggle => {
            // Only toggle visible rows
            const row = toggle.closest('.matrix-row');
            if(row.style.display !== 'none') {
                toggle.checked = checked;
            }
        });
        updateCount();
    }
    
    function updateCount() {
        const active = document.querySelectorAll('.matrix-toggle:checked').length;
        document.getElementById('active-perms-count').innerText = active;
    }
</script>
{% endblock %}
"""

with open('templates/role_permissions.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
