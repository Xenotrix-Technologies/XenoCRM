import re

with open('templates/finance_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_layout = """    <!-- Main Content Panels -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        <!-- Expense Categories Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-indigo-50 text-indigo-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">category</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Expense Categories</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('add-finance-modal')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ finance_categories|length }}</span>
                </div>
            </div>
            
            <ul class="space-y-4">
                {% for cat in finance_categories %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
                        <span class="text-sm text-on-surface font-medium">{{ cat.name }}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button type="button" onclick="openEditFinanceModal('{{ cat.id }}', '{{ cat.name|escapejs }}')" class="p-1.5 rounded-lg hover:bg-surface-variant text-outline hover:text-primary transition-colors" title="Edit Category">
                            <span class="material-symbols-outlined text-[16px]">edit</span>
                        </button>
                        <button type="button" onclick="deleteFinanceCategory('{{ cat.id }}', '{{ cat.name|escapejs }}')" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" title="Delete Category">
                            <span class="material-symbols-outlined text-[16px]">delete</span>
                        </button>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No categories found.</li>
                {% endfor %}
            </ul>
        </div>

        <!-- Payment Methods Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-blue-50 text-blue-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">payments</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Payment Methods</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('add-finance-method-modal')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ finance_methods|length }}</span>
                </div>
            </div>
            
            <ul class="space-y-4">
                {% for method in finance_methods %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
                        <span class="text-sm text-on-surface font-medium">{{ method.name }}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button type="button" onclick="openEditFinanceMethodModal('{{ method.id }}', '{{ method.name|escapejs }}')" class="p-1.5 rounded-lg hover:bg-surface-variant text-outline hover:text-primary transition-colors" title="Edit Payment Method">
                            <span class="material-symbols-outlined text-[16px]">edit</span>
                        </button>
                        <button type="button" onclick="deleteFinanceMethod('{{ method.id }}', '{{ method.name|escapejs }}')" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" title="Delete Payment Method">
                            <span class="material-symbols-outlined text-[16px]">delete</span>
                        </button>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No payment methods found.</li>
                {% endfor %}
            </ul>
        </div>
        
    </div>

    <!-- Modals for Adding -->
    <!-- Add Finance Category Modal -->
    <div id="add-finance-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-[100] flex items-center justify-center hidden">
        <div class="bg-white rounded-2xl w-full max-w-md p-6 shadow-2xl border border-outline-variant/30">
            <div class="flex justify-between items-center mb-4 pb-3 border-b border-outline-variant/20">
                <h3 class="font-headline-md text-headline-md font-bold text-on-background">Add Expense Category</h3>
                <button type="button" onclick="closeModal('add-finance-modal')" class="material-symbols-outlined text-outline hover:text-primary">close</button>
            </div>
            <form id="add-finance-form-modal" method="POST" action="{% url 'add_finance_category' %}" class="space-y-4">
                {% csrf_token %}
                <div>
                    <label class="block text-label-md font-label-md text-outline uppercase mb-1">Category Name *</label>
                    <input type="text" name="name" required class="w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary" />
                </div>
                <div class="mt-6 flex justify-end gap-3 border-t border-outline-variant/20 pt-4">
                    <button type="button" onclick="closeModal('add-finance-modal')" class="px-4 py-2 border border-outline-variant text-secondary rounded-lg hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="px-5 py-2 bg-primary text-on-primary font-button rounded-lg shadow hover:opacity-90">Add Category</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Add Finance Method Modal -->
    <div id="add-finance-method-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-[100] flex items-center justify-center hidden">
        <div class="bg-white rounded-2xl w-full max-w-md p-6 shadow-2xl border border-outline-variant/30">
            <div class="flex justify-between items-center mb-4 pb-3 border-b border-outline-variant/20">
                <h3 class="font-headline-md text-headline-md font-bold text-on-background">Add Payment Method</h3>
                <button type="button" onclick="closeModal('add-finance-method-modal')" class="material-symbols-outlined text-outline hover:text-primary">close</button>
            </div>
            <form id="add-finance-method-form-modal" method="POST" action="{% url 'add_finance_method' %}" class="space-y-4">
                {% csrf_token %}
                <div>
                    <label class="block text-label-md font-label-md text-outline uppercase mb-1">Method Name *</label>
                    <input type="text" name="name" required class="w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary" />
                </div>
                <div class="mt-6 flex justify-end gap-3 border-t border-outline-variant/20 pt-4">
                    <button type="button" onclick="closeModal('add-finance-method-modal')" class="px-4 py-2 border border-outline-variant text-secondary rounded-lg hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="px-5 py-2 bg-primary text-on-primary font-button rounded-lg shadow hover:opacity-90">Add Method</button>
                </div>
            </form>
        </div>
    </div>"""

pattern = re.compile(r'<!-- Main Content Panels -->.*?<!-- Edit Finance Category Modal -->', re.DOTALL)
new_content = re.sub(pattern, new_layout + '\n\n    <!-- Edit Finance Category Modal -->', content)

# Update Javascript form targets since we renamed the IDs for add forms
new_content = new_content.replace("getElementById('add-finance-form')", "getElementById('add-finance-form-modal')")
new_content = new_content.replace("getElementById('add-finance-method-form')", "getElementById('add-finance-method-form-modal')")

# Add openModal and closeModal global JS if missing
if "function openModal" not in new_content:
    js_to_add = """
    function openModal(id) {
        document.getElementById(id).classList.remove('hidden');
    }
    function closeModal(id) {
        document.getElementById(id).classList.add('hidden');
    }
"""
    new_content = new_content.replace("</script>", js_to_add + "\n</script>")

with open('templates/finance_settings.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
