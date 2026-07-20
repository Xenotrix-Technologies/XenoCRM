import os

with open('templates/role_permissions.html', 'r', encoding='utf-8') as f:
    content = f.read()

# I need to replace the loadPermissionsForTarget and savePermissions functions to use the `${roleLower}_${page}` pattern.

# First, modify the button for staff to pass the role name
old_staff_btn = """onclick="selectTarget('staff', '{{ staff.id }}', '{{ staff.user.get_full_name|default:staff.user.username|escapejs }}', '{{ staff.role.name|default:"Employee"|escapejs }}')\""""
new_staff_btn = """onclick="selectTarget('staff', '{{ staff.id }}', '{{ staff.user.get_full_name|default:staff.user.username|escapejs }}', '{{ staff.role.name|escapejs }}')\""""
content = content.replace(old_staff_btn, new_staff_btn)

# Now rewrite the javascript block
new_js = """
<script>
    let currentType = 'role';
    let currentId = null;
    let currentRolePrefix = '';
    
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
        
        // Base Role determines the JSON keys for permissions
        if (type === 'role') {
            currentRolePrefix = id.toLowerCase();
        } else {
            currentRolePrefix = (subText || 'employee').toLowerCase();
        }
        
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
            document.getElementById('selected-target-badge2').innerText = subText || "No Role";
            document.getElementById('override-alert').classList.remove('hidden');
            document.getElementById('selected-target-desc').innerText = "Custom override permissions for this employee.";
        }
        
        // Load permissions
        loadPermissionsForTarget();
    }

    const pagesList = [
        'dashboard', 'leads', 'calendar', 'clients', 'support', 'projects', 'agreements', 
        'staff', 'hr', 'campaigns', 'content_tracker', 'finance', 'settings', 'role_permissions'
    ];

    function loadPermissionsForTarget() {
        if (!currentId) return;
        
        document.querySelectorAll('.matrix-toggle').forEach(el => el.checked = false);
        
        const p = currentType === 'role' ? (rolePermissionsData[currentId] || {}) : (staffPermissionsData[currentId] || {});
        
        pagesList.forEach(page => {
            const viewKey = `${currentRolePrefix}_${page}`;
            const editKey = `${currentRolePrefix}_${page}_edit`;
            const deleteKey = `${currentRolePrefix}_${page}_delete`;
            
            const viewCb = document.getElementById(`perm-${page}`);
            const editCb = document.getElementById(`perm-${page}-edit`);
            const deleteCb = document.getElementById(`perm-${page}-delete`);
            
            if (viewCb && p[viewKey] !== undefined) viewCb.checked = p[viewKey] === true || p[viewKey] === 'true';
            if (editCb && p[editKey] !== undefined) editCb.checked = p[editKey] === true || p[editKey] === 'true';
            if (deleteCb && p[deleteKey] !== undefined) deleteCb.checked = p[deleteKey] === true || p[deleteKey] === 'true';
        });
        
        updateCount();
    }

    function savePermissions() {
        if (!currentId) return;

        const overlay = document.getElementById('loading-overlay');
        overlay.classList.remove('hidden');

        const perms = {};
        pagesList.forEach(page => {
            const viewCb = document.getElementById(`perm-${page}`);
            const editCb = document.getElementById(`perm-${page}-edit`);
            const deleteCb = document.getElementById(`perm-${page}-delete`);
            
            if (viewCb) perms[`${currentRolePrefix}_${page}`] = viewCb.checked;
            if (editCb) perms[`${currentRolePrefix}_${page}_edit`] = editCb.checked;
            if (deleteCb) perms[`${currentRolePrefix}_${page}_delete`] = deleteCb.checked;
        });

        const payload = {
            type: currentType,
            id: currentId,
            permissions: perms
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
                if (currentType === 'role') {
                    rolePermissionsData[currentId] = payload.permissions;
                } else {
                    staffPermissionsData[currentId] = payload.permissions;
                }
                
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
        document.querySelectorAll('.perm-tab').forEach(el => {
            el.classList.remove('text-primary', 'border-primary');
            el.classList.add('text-secondary', 'border-transparent');
        });
        const activeTab = document.getElementById('tab-' + cat);
        activeTab.classList.remove('text-secondary', 'border-transparent');
        activeTab.classList.add('text-primary', 'border-primary');

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
"""

# Extract the <script> block and replace it
start_idx = content.find('<script>\n    let currentType')
if start_idx == -1:
    print("Could not find script block")
else:
    end_idx = content.find('</script>\n{% endblock %}', start_idx)
    content = content[:start_idx] + new_js + content[end_idx+9:]
    with open('templates/role_permissions.html', 'w', encoding='utf-8') as f:
        f.write(content)
