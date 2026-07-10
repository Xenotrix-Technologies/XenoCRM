from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda r: redirect('dashboard'), name='root'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('leads/', views.leads_view, name='leads'),
    path('leads/add/', views.add_lead, name='add_lead'),
    path('leads/import/', views.import_leads, name='import_leads'),
    path('leads/<int:lead_id>/edit/', views.edit_lead, name='edit_lead'),
    path('leads/<int:lead_id>/delete/', views.delete_lead, name='delete_lead'),
    path('leads/<int:lead_id>/json/', views.lead_json_view, name='lead_json'),
    path('pipeline/', views.pipeline_view, name='pipeline'),
    path('pipeline/update-stage/', views.update_lead_stage, name='update_lead_stage'),
    path('leads/<int:lead_id>/', views.contact_detail_view, name='contact_detail'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('activity/log/', views.log_activity, name='log_activity'),
    path('lead/quick-create/', views.quick_create_lead, name='quick_create_lead'),

    path('clients/', views.clients_view, name='clients'),
    path('clients/profile/<path:company_name>/', views.client_profile_view, name='client_profile'),
    path('clients/service/<str:service_id>/', views.service_clients_view, name='service_clients'),
    path('clients/edit-company/', views.edit_client_company, name='edit_client_company'),
    path('clients/delete-company/', views.delete_client_company, name='delete_client_company'),

    path('customer-support/', views.customer_support_view, name='customer_support'),
    path('customer-support/ticket/create/', views.create_ticket, name='create_ticket'),
    path('customer-support/ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('customer-support/ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    path('projects/', views.projects_view, name='projects'),
    path('agreements/', views.agreements_list_view, name='agreements'),
    path('agreements/create/', views.create_agreement_view, name='create_agreement'),
    path('agreements/<int:agreement_id>/', views.agreement_print_view, name='agreement_detail'),
    path('agreements/<int:agreement_id>/edit/', views.update_agreement_view, name='edit_agreement'),
    path('agreements/<int:agreement_id>/delete/', views.delete_agreement_view, name='delete_agreement'),
    path('agreements/<int:agreement_id>/print/', views.agreement_print_view, name='print_agreement'),
    path('reports/', lambda r: redirect('agreements')),
    path('quotations/', lambda r: redirect('agreements')),

    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/list/', views.calendar_list_view, name='calendar_list'),
    path('calendar/create/', views.event_create_view, name='event_create'),
    path('calendar/edit/<int:event_id>/', views.event_edit_view, name='event_edit'),
    path('calendar/delete/<int:event_id>/', views.event_delete_view, name='event_delete'),
    path('calendar/events-json/', views.calendar_events_json_view, name='calendar_events_json'),
    path('calendar/create-ajax/', views.event_create_ajax, name='event_create_ajax'),
    path('calendar/edit-ajax/<int:event_id>/', views.event_edit_ajax, name='event_edit_ajax'),
    path('calendar/delete-ajax/<int:event_id>/', views.event_delete_ajax, name='event_delete_ajax'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('campaign/', views.campaign_view, name='campaign'),
    path('campaign/add/', views.add_campaign, name='add_campaign'),
    path('campaign/<int:campaign_id>/edit/', views.edit_campaign, name='edit_campaign'),
    path('campaign/<int:campaign_id>/delete/', views.delete_campaign, name='delete_campaign'),

    # Lead Status Management
    
    path('statuses/leads/', views.lead_status_settings, name='lead_status_settings'),
    path('statuses/clients/', views.client_status_settings, name='client_status_settings'),
    path('statuses/projects/', views.project_status_settings, name='project_status_settings'),
    path('statuses/campaigns/', views.campaign_status_settings, name='campaign_status_settings'),
    path('statuses/calendar/', views.calendar_status_settings, name='calendar_status_settings'),
    path('statuses/tickets/', views.ticket_status_settings, name='ticket_status_settings'),
    path('statuses/priority/', views.priority_status_settings, name='priority_status_settings'),

    path('statuses/add/', views.add_lead_status, name='add_lead_status'),
    path('statuses/<int:status_id>/edit/', views.edit_lead_status, name='edit_lead_status'),
    path('statuses/<int:status_id>/delete/', views.delete_lead_status, name='delete_lead_status'),
    path('statuses/reorder/', views.reorder_lead_statuses, name='reorder_lead_statuses'),

    # Dynamic Status Management
    path('statuses/category/<str:category>/add/', views.add_dynamic_status, name='add_dynamic_status'),
    path('statuses/category/<str:category>/<int:status_id>/edit/', views.edit_dynamic_status, name='edit_dynamic_status'),
    path('statuses/category/<str:category>/<int:status_id>/delete/', views.delete_dynamic_status, name='delete_dynamic_status'),
    path('statuses/category/<str:category>/reorder/', views.reorder_dynamic_statuses, name='reorder_dynamic_statuses'),
    
    # Finance Payment Methods
    path('statuses/finance-method/add/', views.add_finance_method, name='add_finance_method'),
    path('statuses/finance-method/<int:method_id>/edit/', views.edit_finance_method, name='edit_finance_method'),
    path('statuses/finance-method/<int:method_id>/delete/', views.delete_finance_method, name='delete_finance_method'),

    # Finance Expense Categories
    path('statuses/finance-category/add/', views.add_finance_category, name='add_finance_category'),
    path('statuses/finance-category/<int:cat_id>/edit/', views.edit_finance_category, name='edit_finance_category'),
    path('statuses/finance-category/<int:cat_id>/delete/', views.delete_finance_category, name='delete_finance_category'),

    # Staff Management
    path('staff/', views.staff_list_view, name='staff'),
    path('staff/add/', views.add_staff_view, name='add_staff'),
    path('staff/<int:profile_id>/edit/', views.edit_staff_view, name='edit_staff'),
    path('staff/<int:profile_id>/delete/', views.delete_staff_ajax, name='delete_staff'),

    # Staff Roles Management
    path('staff/roles/', views.staff_roles_view, name='staff_roles'),
    path('staff/roles/add/', views.add_staff_role, name='add_staff_role'),
    path('staff/roles/<int:role_id>/edit/', views.edit_staff_role, name='edit_staff_role'),
    path('staff/roles/<int:role_id>/delete/', views.delete_staff_role, name='delete_staff_role'),

    # Service Management
    path('services/', views.services_view, name='services'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('settings/notifications/', views.notification_settings_view, name='notification_settings'),
    path('settings/permissions/', views.role_permissions_view, name='role_permissions'),
    path('settings/departments/', views.departments_view, name='departments'),
    path('settings/departments/add/', views.add_department, name='add_department'),
    path('settings/departments/<int:department_id>/edit/', views.edit_department, name='edit_department'),
    path('settings/departments/<int:department_id>/delete/', views.delete_department, name='delete_department'),
    path('settings/departments/assign-staff/', views.assign_staff_to_department, name='assign_staff_to_department'),
    path('settings/content-tracker/', views.content_tracker_view, name='content_tracker'),
    path('settings/content-tracker/add/', views.add_content_item, name='add_content_item'),
    path('settings/content-tracker/<int:item_id>/edit/', views.edit_content_item, name='edit_content_item'),
    path('settings/content-tracker/<int:item_id>/delete/', views.delete_content_item, name='delete_content_item'),
    path('settings/content-tracker/<int:item_id>/duplicate/', views.duplicate_content_item, name='duplicate_content_item'),
    path('settings/content-tracker/<int:item_id>/mark-complete/', views.mark_content_complete, name='mark_content_complete'),
    path('settings/content-tracker/bulk-delete/', views.bulk_delete_content_items, name='bulk_delete_content_items'),
    path('settings/content-tracker/import/', views.import_content_items, name='import_content_items'),
    
    # Editor Board & Dashboard
    path('editor-dashboard/', views.editor_dashboard_view, name='editor_dashboard'),
    path('editor-board/', views.editor_board_view, name='editor_board'),
    path('editor-board/update/', views.editor_board_update, name='editor_board_update'),
    path('post-management/', views.post_management_view, name='post_management'),
    path('post-management/update/', views.post_management_update, name='post_management_update'),
    
    path('settings/content-settings/', views.content_settings_view, name='content_settings'),
    path('settings/content-settings/add/', views.add_content_option, name='add_content_option'),
    path('settings/content-settings/<int:option_id>/edit/', views.edit_content_option, name='edit_content_option'),
    path('settings/content-settings/<int:option_id>/delete/', views.delete_content_option, name='delete_content_option'),
    
    # Finance
    path('finance/dashboard/', views.finance_dashboard_view, name='finance_dashboard'),
    path('finance/income/', views.finance_income_view, name='finance_income'),
    path('finance/income/add/', views.finance_add_income_view, name='finance_add_income'),
    path('finance/income/edit/<int:income_id>/', views.finance_edit_income, name='finance_edit_income'),
    path('finance/expenses/', views.finance_expenses_view, name='finance_expenses'),
    path('finance/expenses/add/', views.finance_add_expense_view, name='finance_add_expense'),
    path('finance/expenses/edit/<int:expense_id>/', views.finance_edit_expense, name='finance_edit_expense'),
    path('finance/reports/', views.finance_reports_view, name='finance_reports'),
    path('finance/partner-payouts/', views.partner_payout_view, name='partner_payouts'),
    path('finance/partner-payouts/add/', views.partner_payout_add_view, name='partner_payout_add'),
    path('finance/settings/', views.finance_settings_view, name='finance_settings'),
]
