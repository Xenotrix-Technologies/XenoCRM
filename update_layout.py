import re

with open('templates/finance_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_layout = """    <!-- Main Content Panels -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 relative">
        <!-- Column 1: Expense Categories -->
        <div class="flex flex-col gap-4">
            <div class="sticky top-4 z-10 bg-background/90 backdrop-blur-md pb-2">
                <h3 class="font-headline-md text-headline-md font-bold text-on-surface border-b border-outline-variant/30 pb-3">Expense Categories</h3>
            </div>
            <div class="space-y-4">
                {% for cat in finance_categories %}
                <div class="group flex items-center justify-between p-6 bg-white dark:bg-surface-container rounded-[16px] border border-outline-variant hover:border-primary/40 shadow-sm hover:shadow transition-all duration-300">
                    <div class="flex items-center gap-3">
                        <span class="px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wider bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
                            {{ cat.name }}
                        </span>
                    </div>
                    <div class="flex items-center gap-1 opacity-60 group-hover:opacity-100 transition-opacity">
                        <button type="button"
                            onclick="openEditFinanceModal('{{ cat.id }}', '{{ cat.name|escapejs }}')"
                            class="p-2 rounded-full hover:bg-surface-variant text-outline hover:text-primary transition-colors"
                            title="Edit Category">
                            <span class="material-symbols-outlined text-[18px]">edit</span>
                        </button>
                        <button type="button" onclick="deleteFinanceCategory('{{ cat.id }}', '{{ cat.name|escapejs }}')"
                            class="p-2 rounded-full hover:bg-red-50 text-outline hover:text-red-600 transition-colors"
                            title="Delete Category">
                            <span class="material-symbols-outlined text-[18px]">delete</span>
                        </button>
                    </div>
                </div>
                {% empty %}
                <div class="p-8 text-center text-outline bg-white dark:bg-surface-container rounded-[16px] border border-outline-variant/50 border-dashed">
                    No categories found. Add a new one below.
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Column 2: Payment Methods -->
        <div class="flex flex-col gap-4">
            <div class="sticky top-4 z-10 bg-background/90 backdrop-blur-md pb-2">
                <h3 class="font-headline-md text-headline-md font-bold text-on-surface border-b border-outline-variant/30 pb-3">Payment Methods</h3>
            </div>
            <div class="space-y-4">
                {% for method in finance_methods %}
                <div class="group flex items-center justify-between p-6 bg-white dark:bg-surface-container rounded-[16px] border border-outline-variant hover:border-primary/40 shadow-sm hover:shadow transition-all duration-300">
                    <div class="flex items-center gap-3">
                        <span class="px-3 py-1 rounded-md text-xs font-bold uppercase tracking-wider bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
                            {{ method.name }}
                        </span>
                    </div>
                    <div class="flex items-center gap-1 opacity-60 group-hover:opacity-100 transition-opacity">
                        <button type="button"
                            onclick="openEditFinanceMethodModal('{{ method.id }}', '{{ method.name|escapejs }}')"
                            class="p-2 rounded-full hover:bg-surface-variant text-outline hover:text-primary transition-colors"
                            title="Edit Payment Method">
                            <span class="material-symbols-outlined text-[18px]">edit</span>
                        </button>
                        <button type="button" onclick="deleteFinanceMethod('{{ method.id }}', '{{ method.name|escapejs }}')"
                            class="p-2 rounded-full hover:bg-red-50 text-outline hover:text-red-600 transition-colors"
                            title="Delete Payment Method">
                            <span class="material-symbols-outlined text-[18px]">delete</span>
                        </button>
                    </div>
                </div>
                {% empty %}
                <div class="p-8 text-center text-outline bg-white dark:bg-surface-container rounded-[16px] border border-outline-variant/50 border-dashed">
                    No payment methods found. Add a new one below.
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Column 3: Create New Records -->
        <div class="flex flex-col gap-4">
            <div class="sticky top-4 z-10 bg-background/90 backdrop-blur-md pb-2">
                <h3 class="font-headline-md text-headline-md font-bold text-on-surface border-b border-outline-variant/30 pb-3">Create New Records</h3>
            </div>
            
            <div class="space-y-6">
                <div id="add-finance-form" class="space-y-6">
                    <!-- Finance Category Form -->
                    <div class="bg-white dark:bg-surface-container rounded-[16px] p-6 shadow-sm border border-outline-variant">
                        <form method="POST" action="{% url 'add_finance_category' %}" class="space-y-4">
                            {% csrf_token %}
                            <div>
                                <h4 class="font-bold text-on-surface mb-4 text-sm uppercase flex items-center gap-2">
                                    <span class="material-symbols-outlined text-primary text-[18px]">category</span>
                                    Add Expense Category
                                </h4>
                                <label class="block text-label-md font-label-md text-outline uppercase mb-2">Category Name *</label>
                                <input type="text" name="name" required placeholder="e.g. Marketing"
                                    class="w-full bg-surface-container-low border border-outline-variant rounded-xl px-4 py-3 text-body-sm focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none" />
                            </div>
                            <button type="submit"
                                class="w-full bg-primary text-on-primary py-3 rounded-xl font-button hover:bg-primary/90 transition-all shadow hover:shadow-md flex items-center justify-center gap-2">
                                <span class="material-symbols-outlined text-[18px]">add</span>
                                Add Category
                            </button>
                        </form>
                    </div>

                    <!-- Finance Method Form -->
                    <div class="bg-white dark:bg-surface-container rounded-[16px] p-6 shadow-sm border border-outline-variant">
                        <form id="add-finance-method-form" method="POST" action="{% url 'add_finance_method' %}" class="space-y-4">
                            {% csrf_token %}
                            <div>
                                <h4 class="font-bold text-on-surface mb-4 text-sm uppercase flex items-center gap-2">
                                    <span class="material-symbols-outlined text-primary text-[18px]">payments</span>
                                    Add Payment Method
                                </h4>
                                <label class="block text-label-md font-label-md text-outline uppercase mb-2">Method Name *</label>
                                <input type="text" name="name" required placeholder="e.g. Credit Card"
                                    class="w-full bg-surface-container-low border border-outline-variant rounded-xl px-4 py-3 text-body-sm focus:ring-2 focus:ring-primary focus:border-transparent transition-all outline-none" />
                            </div>
                            <button type="submit"
                                class="w-full bg-primary text-on-primary py-3 rounded-xl font-button hover:bg-primary/90 transition-all shadow hover:shadow-md flex items-center justify-center gap-2">
                                <span class="material-symbols-outlined text-[18px]">add</span>
                                Add Method
                            </button>
                        </form>
                    </div>
                </div>
                
                <!-- Helpful Tip -->
                <div class="rounded-[16px] p-6 border border-primary/20 bg-primary-container/10">
                    <div class="flex items-start gap-3">
                        <span class="material-symbols-outlined text-primary mt-1">lightbulb</span>
                        <div>
                            <h4 class="font-bold text-on-surface mb-1 text-sm">Helpful Tip</h4>
                            <p class="text-body-sm text-secondary leading-relaxed">
                                These categories appear when adding or editing an income or expense record.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>"""

# Replace the entire old grid container with the new layout
pattern = re.compile(r'<!-- Main Content Panels -->.*?<!-- Edit Finance Category Modal -->', re.DOTALL)
new_content = re.sub(pattern, new_layout + '\n\n    <!-- Edit Finance Category Modal -->', content)

with open('templates/finance_settings.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
