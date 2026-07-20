import re

with open('templates/hr_settings.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_layout = """    <!-- Main Content Panels -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mt-6">
        
        <!-- Leave Types Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-indigo-50 text-indigo-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">beach_access</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Leave Types</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('modal-leave')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ leave_types|length }}</span>
                </div>
            </div>
            <ul class="space-y-4">
                {% for item in leave_types %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full {% if item.is_active %}bg-emerald-400{% else %}bg-red-400{% endif %}"></div>
                        <span class="text-sm text-on-surface font-medium">{{ item.name }}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <form method="POST" style="display: inline;" class="m-0 p-0 h-6">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="delete_leave_type">
                            <input type="hidden" name="item_id" value="{{ item.id }}">
                            <button type="submit" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" onclick="return confirm('Are you sure?')">
                                <span class="material-symbols-outlined text-[16px]">delete</span>
                            </button>
                        </form>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No leave types found.</li>
                {% endfor %}
            </ul>
        </div>

        <!-- Leave Request Statuses Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">approval</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Leave Statuses</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('modal-leave_request')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ leave_request_statuses|length }}</span>
                </div>
            </div>
            <ul class="space-y-4">
                {% for item in leave_request_statuses %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full {% if item.is_active %}bg-emerald-400{% else %}bg-red-400{% endif %}"></div>
                        <span class="text-sm text-on-surface font-medium">{{ item.name }}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <form method="POST" style="display: inline;" class="m-0 p-0 h-6">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="delete_leave_request_status">
                            <input type="hidden" name="item_id" value="{{ item.id }}">
                            <button type="submit" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" onclick="return confirm('Are you sure?')">
                                <span class="material-symbols-outlined text-[16px]">delete</span>
                            </button>
                        </form>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No leave statuses found.</li>
                {% endfor %}
            </ul>
        </div>

        <!-- Attendance Statuses Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-emerald-50 text-emerald-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">fact_check</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Attendance</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('modal-attendance')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ attendance_statuses|length }}</span>
                </div>
            </div>
            <ul class="space-y-4">
                {% for item in attendance_statuses %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full {% if item.is_active %}bg-emerald-400{% else %}bg-red-400{% endif %}"></div>
                        <span class="text-sm text-on-surface font-medium">{{ item.name }}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <form method="POST" style="display: inline;" class="m-0 p-0 h-6">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="delete_attendance_status">
                            <input type="hidden" name="item_id" value="{{ item.id }}">
                            <button type="submit" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" onclick="return confirm('Are you sure?')">
                                <span class="material-symbols-outlined text-[16px]">delete</span>
                            </button>
                        </form>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No attendance statuses found.</li>
                {% endfor %}
            </ul>
        </div>

        <!-- Payroll Rules Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-purple-50 text-purple-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">payments</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Payroll Rules</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('modal-payroll')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ payroll_rules|length }}</span>
                </div>
            </div>
            <ul class="space-y-4">
                {% for item in payroll_rules %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
                        <span class="text-sm text-on-surface font-medium">{{ item.name }}</span>
                        <span class="text-xs text-secondary ml-1 bg-surface-variant/50 px-2 rounded">{{ item.amount }}{% if item.is_percentage %}%{% else %}${% endif %}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <form method="POST" style="display: inline;" class="m-0 p-0 h-6">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="delete_payroll_rule">
                            <input type="hidden" name="item_id" value="{{ item.id }}">
                            <button type="submit" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" onclick="return confirm('Are you sure?')">
                                <span class="material-symbols-outlined text-[16px]">delete</span>
                            </button>
                        </form>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No payroll rules found.</li>
                {% endfor %}
            </ul>
        </div>

        <!-- Departments Card -->
        <div class="bg-white dark:bg-surface-container rounded-[24px] p-6 shadow-sm border border-outline-variant/50">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-rose-50 text-rose-500 rounded-xl flex items-center justify-center">
                        <span class="material-symbols-outlined text-[20px]">domain</span>
                    </div>
                    <h3 class="font-bold text-sm tracking-widest text-on-surface uppercase">Departments</h3>
                </div>
                <div class="flex items-center gap-2">
                    <button type="button" onclick="openModal('modal-department')" class="w-7 h-7 rounded-full bg-surface-variant/50 hover:bg-surface-variant flex items-center justify-center text-secondary hover:text-primary transition-colors">
                        <span class="material-symbols-outlined text-[16px]">add</span>
                    </button>
                    <span class="bg-surface-variant text-secondary text-xs font-bold px-2.5 py-1 rounded-full">{{ departments|length }}</span>
                </div>
            </div>
            <ul class="space-y-4">
                {% for item in departments %}
                <li class="group flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
                        <span class="text-sm text-on-surface font-medium">{{ item.name }}</span>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <form method="POST" style="display: inline;" class="m-0 p-0 h-6">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="delete_department">
                            <input type="hidden" name="item_id" value="{{ item.id }}">
                            <button type="submit" class="p-1.5 rounded-lg hover:bg-red-50 text-outline hover:text-red-600 transition-colors" onclick="return confirm('Are you sure?')">
                                <span class="material-symbols-outlined text-[16px]">delete</span>
                            </button>
                        </form>
                    </div>
                </li>
                {% empty %}
                <li class="text-sm text-secondary italic">No departments found.</li>
                {% endfor %}
            </ul>
        </div>
        
    </div>"""

pattern = re.compile(r'<!-- Settings Tabs -->.*?</div>\s*</div>\s*</div>', re.DOTALL)
new_content = re.sub(pattern, new_layout + '\n  </div>\n</div>', content)

# Remove the switchTab script as it's no longer needed
script_pattern = re.compile(r'function switchTab\(tabId\) \{.*?\}.*?(function openModal)', re.DOTALL)
new_content = re.sub(script_pattern, r'\1', new_content)

with open('templates/hr_settings.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
