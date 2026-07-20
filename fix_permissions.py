import re

with open('templates/role_permissions.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add the rolePermissionsData script block before the main <script> tag
if "const rolePermissionsData =" not in content:
    content = content.replace("<script>", "<script>\n    const rolePermissionsData = {{ role_permissions_json|safe }};\n")

# 2. Fix savePermissions fetch URL and payload
old_fetch = """        fetch("{% url 'update_role_permissions' %}", {"""
new_fetch = """        const payload = {
            role: currentRoleName,
            permissions: data.permissions
        };
        fetch("{% url 'role_permissions' %}", {"""
content = content.replace(old_fetch, new_fetch)

# Fix the body of the fetch request
old_body = """            body: JSON.stringify(data)"""
new_body = """            body: JSON.stringify(payload)"""
content = content.replace(old_body, new_body)

# 3. Rewrite loadPermissionsForRole
old_load = """    function loadPermissionsForRole(roleName) {
        // Reset toggles
        document.querySelectorAll('.matrix-toggle').forEach(el => el.checked = false);
        updateCount();
        
        const url = "{% url 'get_role_permissions' %}?role_name=" + encodeURIComponent(roleName);
        fetch(url)
            .then(res => res.json())
            .then(data => {
                if(data.success && data.permissions) {
                    // Populate toggles
                    const p = data.permissions;
                    
                    // Simple mapping function
                    const mapPerm = (id, val) => {
                        const el = document.getElementById(id);
                        if(el) el.checked = val;
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
                    mapPerm('perm-campaigns', p.can_view_campaigns);
                    mapPerm('perm-campaigns-edit', p.can_edit_campaigns);
                    mapPerm('perm-campaigns-delete', p.can_delete_campaigns);
                    mapPerm('perm-staff', p.can_view_staff);
                    mapPerm('perm-staff-edit', p.can_edit_staff);
                    mapPerm('perm-staff-delete', p.can_delete_staff);
                    mapPerm('perm-content_tracker', p.can_view_content_tracker);
                    mapPerm('perm-content_tracker-edit', p.can_edit_content_tracker);
                    mapPerm('perm-content_tracker-delete', p.can_delete_content_tracker);
                    mapPerm('perm-settings', p.can_view_settings);
                    mapPerm('perm-settings-edit', p.can_edit_settings);
                    mapPerm('perm-settings-delete', p.can_delete_settings);
                    mapPerm('perm-role_permissions', p.can_view_role_permissions);
                    mapPerm('perm-role_permissions-edit', p.can_edit_role_permissions);
                    mapPerm('perm-role_permissions-delete', p.can_delete_role_permissions);
                }
                updateCount();
            })
            .catch(err => console.error("Error loading permissions:", err));
    }"""

new_load = """    function loadPermissionsForRole(roleName) {
        // Reset toggles
        document.querySelectorAll('.matrix-toggle').forEach(el => el.checked = false);
        updateCount();
        
        const p = rolePermissionsData[roleName] || {};
        
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
        mapPerm('perm-campaigns', p.can_view_campaigns);
        mapPerm('perm-campaigns-edit', p.can_edit_campaigns);
        mapPerm('perm-campaigns-delete', p.can_delete_campaigns);
        mapPerm('perm-staff', p.can_view_staff);
        mapPerm('perm-staff-edit', p.can_edit_staff);
        mapPerm('perm-staff-delete', p.can_delete_staff);
        mapPerm('perm-content_tracker', p.can_view_content_tracker);
        mapPerm('perm-content_tracker-edit', p.can_edit_content_tracker);
        mapPerm('perm-content_tracker-delete', p.can_delete_content_tracker);
        mapPerm('perm-settings', p.can_view_settings);
        mapPerm('perm-settings-edit', p.can_edit_settings);
        mapPerm('perm-settings-delete', p.can_delete_settings);
        mapPerm('perm-role_permissions', p.can_view_role_permissions);
        mapPerm('perm-role_permissions-edit', p.can_edit_role_permissions);
        mapPerm('perm-role_permissions-delete', p.can_delete_role_permissions);
        
        updateCount();
    }"""

content = content.replace(old_load, new_load)

with open('templates/role_permissions.html', 'w', encoding='utf-8') as f:
    f.write(content)
