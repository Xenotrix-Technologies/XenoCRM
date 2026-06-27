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
    path('calendar/create/', views.event_create_view, name='event_create'),
    path('calendar/edit/<int:event_id>/', views.event_edit_view, name='event_edit'),
    path('calendar/delete/<int:event_id>/', views.event_delete_view, name='event_delete'),
    path('calendar/events-json/', views.calendar_events_json_view, name='calendar_events_json'),
    path('calendar/create-ajax/', views.event_create_ajax, name='event_create_ajax'),
    path('calendar/edit-ajax/<int:event_id>/', views.event_edit_ajax, name='event_edit_ajax'),
    path('calendar/delete-ajax/<int:event_id>/', views.event_delete_ajax, name='event_delete_ajax'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('campaign/', views.campaign_view, name='campaign'),

    # Lead Status Management
    path('statuses/', views.lead_statuses_view, name='lead_statuses'),
    path('statuses/add/', views.add_lead_status, name='add_lead_status'),
    path('statuses/<int:status_id>/edit/', views.edit_lead_status, name='edit_lead_status'),
    path('statuses/<int:status_id>/delete/', views.delete_lead_status, name='delete_lead_status'),
    path('statuses/reorder/', views.reorder_lead_statuses, name='reorder_lead_statuses'),

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
]
