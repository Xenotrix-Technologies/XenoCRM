import os

for filename in ["contact_detail.html", "client_contact_detail.html"]:
    path = os.path.join("templates", filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    js_block = """    document.addEventListener('DOMContentLoaded', function() {
        const statusSelect = document.getElementById('lead-status-select');
        const serviceSelect = document.getElementById('lead-service-select');
        
        function toggleServiceSelect() {
            if (statusSelect && serviceSelect) {
                if (statusSelect.value === 'Qualified') {
                    serviceSelect.disabled = false;
                    serviceSelect.classList.remove('opacity-50', 'cursor-not-allowed');
                } else {
                    serviceSelect.value = "";
                    serviceSelect.disabled = true;
                    serviceSelect.classList.add('opacity-50', 'cursor-not-allowed');
                }
            }
        }
        
        if (statusSelect) {
            statusSelect.addEventListener('change', toggleServiceSelect);
            toggleServiceSelect();
        }
    });"""
    content = content.replace(js_block, "")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Removed JS overrides in templates")
