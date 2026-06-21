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
    path('leads/<int:lead_id>/edit/', views.edit_lead, name='edit_lead'),
    path('leads/<int:lead_id>/json/', views.lead_json_view, name='lead_json'),
    path('pipeline/', views.pipeline_view, name='pipeline'),
    path('pipeline/update-stage/', views.update_lead_stage, name='update_lead_stage'),
    path('leads/<int:lead_id>/', views.contact_detail_view, name='contact_detail'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/complete/', views.complete_task, name='complete_task'),
    path('activity/log/', views.log_activity, name='log_activity'),
    path('lead/quick-create/', views.quick_create_lead, name='quick_create_lead'),

    path('clients/', views.clients_view, name='clients'),

    path('customer-support/', views.customer_support_view, name='customer_support'),
    path('projects/', views.projects_view, name='projects'),
    path('reports/', views.reports_view, name='reports'),

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
    ]
