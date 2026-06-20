import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Organization, UserProfile, Lead, Activity, Task, Meeting, EmailTemplate, HelpArticle, Event, BillingPlan, Subscription
from .forms import EventForm, ProfileForm
# Views for navigation pages with proper multi-tenant database queries

@login_required
def contacts_view(request):
    org = request.user.profile.organization
    leads = Lead.objects.filter(organization=org).order_by('-created_at')
    return render(request, 'contacts.html', {'leads': leads})


@login_required
def accounts_view(request):
    org = request.user.profile.organization
    leads = Lead.objects.filter(organization=org)
    
    accounts_dict = {}
    for lead in leads:
        comp = lead.company
        if not comp:
            continue
        if comp not in accounts_dict:
            accounts_dict[comp] = {
                'company': comp,
                'contacts_count': 0,
                'total_value': 0.0,
                'avg_score': 0,
                'leads': []
            }
        accounts_dict[comp]['contacts_count'] += 1
        accounts_dict[comp]['total_value'] += float(lead.value)
        accounts_dict[comp]['avg_score'] += lead.score
        accounts_dict[comp]['leads'].append(lead)
    
    accounts_list = []
    for comp, data in accounts_dict.items():
        if data['contacts_count'] > 0:
            data['avg_score'] = int(data['avg_score'] / data['contacts_count'])
        accounts_list.append(data)
        
    return render(request, 'accounts.html', {'accounts': accounts_list})


@login_required
def opportunities_view(request):
    org = request.user.profile.organization
    leads = Lead.objects.filter(organization=org).exclude(stage__in=['Won', 'Lost']).order_by('-value')
    return render(request, 'opportunities.html', {'opportunities': leads})


@login_required
def marketing_view(request):
    templates = EmailTemplate.objects.all()
    stats = {
        'email_open_rate': 24.8,
        'click_through_rate': 3.2,
        'subscribers': 1240,
        'campaigns_sent': 18
    }
    return render(request, 'marketing.html', {'templates': templates, 'stats': stats})


@login_required
def customer_support_view(request):
    articles = HelpArticle.objects.all()
    tickets = [
        {'id': 'TCK-102', 'subject': 'API Integration Error', 'status': 'Open', 'priority': 'High', 'created': '1h ago'},
        {'id': 'TCK-101', 'subject': 'Billing Query', 'status': 'Pending', 'priority': 'Medium', 'created': '3h ago'},
        {'id': 'TCK-099', 'subject': 'Password Reset Issue', 'status': 'Closed', 'priority': 'Low', 'created': '1d ago'}
    ]
    return render(request, 'customer_support.html', {'articles': articles, 'tickets': tickets})


@login_required
def projects_view(request):
    org = request.user.profile.organization
    tasks = Task.objects.filter(lead__organization=org).order_by('due_date')
    return render(request, 'projects.html', {'tasks': tasks})


@login_required
def reports_view(request):
    org = request.user.profile.organization
    leads = Lead.objects.filter(organization=org)
    total_value = sum(float(l.value) for l in leads)
    won_value = sum(float(l.value) for l in leads.filter(stage='Won'))
    lost_value = sum(float(l.value) for l in leads.filter(stage='Lost'))
    active_value = total_value - won_value - lost_value
    
    metrics = {
        'total_pipeline': total_value,
        'closed_won': won_value,
        'closed_lost': lost_value,
        'active_pipeline': active_value,
        'lead_count': leads.count()
    }
    return render(request, 'reports.html', {'metrics': metrics})


@login_required
def ai_assistant_view(request):
    org = request.user.profile.organization
    leads = Lead.objects.filter(organization=org)
    hot_leads = leads.filter(score__gte=80).order_by('-score')
    suggestions = []
    for l in hot_leads[:3]:
        suggestions.append(f"Outreach to {l.name} from {l.company} (Score: {l.score}). A high-value opportunity of ${l.value} is ready for Proposal.")
    if not suggestions:
        suggestions.append("No high-score leads found. Consider generating more prospects and scoring them using the Quick Create tool.")
    return render(request, 'ai_assistant.html', {'suggestions': suggestions})


@login_required
def business_view(request):
    org = request.user.profile.organization
    leads = Lead.objects.filter(organization=org)
    total_deals = leads.count()
    won_deals = leads.filter(stage='Won').count()
    win_rate = (won_deals / total_deals * 100) if total_deals > 0 else 0
    avg_deal_value = sum(float(l.value) for l in leads) / total_deals if total_deals > 0 else 0
    
    business_stats = {
        'win_rate': win_rate,
        'avg_deal_value': avg_deal_value,
        'active_deals': leads.exclude(stage__in=['Won', 'Lost']).count(),
        'total_deals': total_deals
    }
    return render(request, 'business.html', {'stats': business_stats})


@login_required
def campaign_view(request):
    campaigns = [
        {'name': 'Summer Solstice Email Blast', 'status': 'Active', 'leads_generated': 42, 'spend': 450.00, 'budget': 1000.00},
        {'name': 'Q2 LinkedIn Lead Gen', 'status': 'Completed', 'leads_generated': 128, 'spend': 1200.00, 'budget': 1200.00},
        {'name': 'AdWords CRM Search Retargeting', 'status': 'Active', 'leads_generated': 19, 'spend': 280.00, 'budget': 800.00},
        {'name': 'Autumn Product Demo Invite', 'status': 'Planning', 'leads_generated': 0, 'spend': 0.00, 'budget': 500.00}
    ]
    return render(request, 'campaign.html', {'campaigns': campaigns})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        org_name = request.POST.get('org_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration/signup.html')

        try:
            # Create Organization
            org = Organization.objects.create(name=org_name)
            
            # Create User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create UserProfile
            # Auto-assign typical premium avatar urls to make it visually pleasing
            avatar_url = "https://lh3.googleusercontent.com/aida-public/AB6AXuAW7b6-rqX4pvH0f9U4MhDYRZg0b0CU4zdddcnQDxuSKVC4o7zD5quJU0Yr0vS_mW_ZpyNm2rNU1ZtClVgLMkxLZZtMoQdkY_jpsH2UiHW0mX7f97C822jCC7YFuBcHyUSk2RY-hXiu4fgyIL51dfNAQ_yLS_pTp-ebecMCF--zR2e-ZBC3zN3LNFES0Gs8aXbIQ5GXtVkf9lIX_HFRCZwopPHKEocY22oY2KtZxnI8Cl98c0sK5MQwclQW1Cs0hLmHW2awzgfmQK8l"
            UserProfile.objects.create(
                user=user,
                organization=org,
                role="Administrator",
                profile_image_url=avatar_url
            )

            # Log user in
            login(request, user)
            messages.success(request, f"Welcome to XenoCRM, {first_name}! Your organization space '{org_name}' has been created.")
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error during signup: {str(e)}")
            return render(request, 'registration/signup.html')

    return render(request, 'registration/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'registration/login.html')
            
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    org = request.user.profile.organization
    
    # Base leads query
    leads_qs = Lead.objects.filter(organization=org)
    
    # 1. Total Revenue (Value of leads in 'Won' stage)
    won_leads = leads_qs.filter(stage='Won')
    total_revenue = won_leads.aggregate(Sum('value'))['value__sum'] or 0.00
    
    # 2. Total Leads Count
    total_leads = leads_qs.count()
    
    # 3. Conversion Rate (Won Leads / Total Leads)
    conversion_rate = (won_leads.count() / total_leads * 100) if total_leads > 0 else 0.0
    
    # 4. Pending Tasks count
    tasks_qs = Task.objects.filter(lead__organization=org)
    active_tasks_count = tasks_qs.filter(completed=False).count()
    completed_tasks_count = tasks_qs.filter(completed=True).count()
    total_tasks_count = tasks_qs.count()
    task_completion_rate = (completed_tasks_count / total_tasks_count * 100) if total_tasks_count > 0 else 0.0
    
    # 5. New Leads (ordered by created_at desc)
    new_leads = leads_qs.order_by('-created_at')
    
    # 6. Recent activities
    recent_activities = Activity.objects.filter(lead__organization=org).order_by('-timestamp')[:5]
    
    # 7. Upcoming meetings
    upcoming_meetings = Meeting.objects.filter(organization=org, date_time__gte=timezone.now()).order_by('date_time')[:3]
    
    # 8. Sales Funnel stats (stage counts)
    stages = ['New', 'Qualified', 'Proposal', 'Negotiation', 'Won']
    funnel_data = {}
    for st in stages:
        funnel_data[st] = leads_qs.filter(stage=st).count()
        
    prospects_count = funnel_data['New']
    funnel_rates = {}
    for st in stages:
        if prospects_count > 0:
            funnel_rates[st] = (funnel_data[st] / prospects_count) * 100
        else:
            funnel_rates[st] = 0.0 if st != 'New' else 100.0

    # 9. AI Insights (Generated dynamically based on leads)
    ai_insights = []
    hot_leads = leads_qs.filter(score__gte=85).order_by('-score')
    for hl in hot_leads[:2]:
        ai_insights.append({
            'title': 'Opportunity Found',
            'type': 'HOT',
            'time': 'Just now',
            'description': f"Lead '{hl.name}' from {hl.company} has a high score of {hl.score}. Recommended outreach for proposal."
        })
    cold_leads = leads_qs.filter(status='Cold Lead')
    for cl in cold_leads[:1]:
        ai_insights.append({
            'title': 'Cold Lead Alert',
            'type': 'CHURN',
            'time': '2h ago',
            'description': f"Engagement for lead '{cl.name}' has dropped. Risk of churn: Medium."
        })
    if not ai_insights:
        ai_insights.append({
            'title': 'Outreach Tip',
            'type': 'TIP',
            'time': '1h ago',
            'description': "Ensure all New leads have an assigned owner and a scheduled initial activity."
        })

    context = {
        'total_revenue': total_revenue,
        'total_leads': total_leads,
        'conversion_rate': conversion_rate,
        'active_tasks_count': active_tasks_count,
        'completed_tasks_count': completed_tasks_count,
        'task_completion_rate': task_completion_rate,
        'new_leads': new_leads,
        'recent_activities': recent_activities,
        'upcoming_meetings': upcoming_meetings,
        'funnel_data': funnel_data,
        'funnel_rates': funnel_rates,
        'ai_insights': ai_insights,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def leads_view(request):
    org = request.user.profile.organization
    
    # Export CSV handler
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leads_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Company', 'Score', 'Status', 'Stage', 'Value', 'Owner', 'Lifecycle Stage', 'Annual Revenue', 'Health Score'])
        
        leads_export = Lead.objects.filter(organization=org)
        for lead in leads_export:
            owner_name = lead.owner.user.get_full_name() if lead.owner else 'None'
            writer.writerow([lead.name, lead.email, lead.company, lead.score, lead.status, lead.stage, lead.value, owner_name, lead.lifecycle_stage, lead.annual_revenue, lead.health_score])
        return response
        
    # Bulk actions POST handler
    if request.method == 'POST':
        action = request.POST.get('bulk_action')
        lead_ids = request.POST.getlist('lead_ids')
        if action and lead_ids:
            target_leads = Lead.objects.filter(id__in=lead_ids, organization=org)
            if action == 'delete':
                count = target_leads.count()
                target_leads.delete()
                messages.success(request, f"Successfully deleted {count} leads.")
            elif action == 'change_status_qualified':
                count = target_leads.update(status='Qualified', stage='Qualified')
                for lead in target_leads:
                    Activity.objects.create(
                        lead=lead,
                        type='Stage Update',
                        description="Bulk changed status to Qualified."
                    )
                messages.success(request, f"Successfully updated {count} leads to Qualified.")
        return redirect('leads')

    leads_qs = Lead.objects.filter(organization=org)
    
    # 1. Search Query
    q = request.GET.get('q', '').strip()
    if q:
        leads_qs = leads_qs.filter(
            Q(name__icontains=q) | 
            Q(company__icontains=q) | 
            Q(email__icontains=q)
        )
        
    # 2. Filters
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        leads_qs = leads_qs.filter(status=status_filter)
        
    owner_filter = request.GET.get('owner', '').strip()
    if owner_filter:
        leads_qs = leads_qs.filter(owner_id=owner_filter)
        
    # 3. Sorting
    sort_by = request.GET.get('sort', 'score_desc').strip()
    if sort_by == 'score_asc':
        leads_qs = leads_qs.order_by('score')
    elif sort_by == 'value_desc':
        leads_qs = leads_qs.order_by('-value')
    elif sort_by == 'value_asc':
        leads_qs = leads_qs.order_by('value')
    else: # default score_desc
        leads_qs = leads_qs.order_by('-score')

    # Owners lookup
    owners = UserProfile.objects.filter(organization=org)
    
    # Pagination
    paginator = Paginator(leads_qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'leads': page_obj,
        'owners': owners,
        'status_filter': status_filter,
        'owner_filter': owner_filter,
        'sort_by': sort_by,
        'q': q,
        'paginator': paginator
    }
    
    return render(request, 'leads.html', context)

@login_required
def pipeline_view(request):
    org = request.user.profile.organization
    leads_qs = Lead.objects.filter(organization=org)
    
    # Calculate Forecast details
    total_pipeline = leads_qs.aggregate(Sum('value'))['value__sum'] or 0.00
    won_leads = leads_qs.filter(stage='Won')
    total_deals = leads_qs.count()
    win_rate = (won_leads.count() / total_deals * 100) if total_deals > 0 else 0.0
    weighted_forecast = float(total_pipeline) * 0.25 # Simple weighted forecast metric
    
    # Group leads by stage
    stages = ['New', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost']
    pipeline_stages = {}
    for st in stages:
        stage_leads = leads_qs.filter(stage=st)
        stage_total = stage_leads.aggregate(Sum('value'))['value__sum'] or 0.00
        pipeline_stages[st] = {
            'leads': stage_leads,
            'total_value': stage_total
        }
        
    owners = UserProfile.objects.filter(organization=org)

    context = {
        'weighted_forecast': weighted_forecast,
        'total_pipeline': total_pipeline,
        'total_deals': total_deals,
        'win_rate': win_rate,
        'pipeline_stages': pipeline_stages,
        'owners': owners
    }
    
    return render(request, 'pipeline.html', context)

@login_required
def update_lead_stage(request):
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        stage = request.POST.get('stage')
        org = request.user.profile.organization
        
        try:
            lead = Lead.objects.get(id=lead_id, organization=org)
            old_stage = lead.stage
            lead.stage = stage
            # Align status
            if stage in ['New', 'Qualified', 'Lost']:
                lead.status = stage
            elif stage in ['Proposal', 'Negotiation']:
                lead.status = 'Contacted'
            elif stage == 'Won':
                lead.status = 'Qualified'
            lead.save()
            
            # Log activity
            Activity.objects.create(
                lead=lead,
                type='Stage Update',
                description=f"Moved stage from {old_stage} to {stage}."
            )
            return JsonResponse({'success': True})
        except Lead.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lead not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def contact_detail_view(request, lead_id):
    org = request.user.profile.organization
    try:
        lead = Lead.objects.get(id=lead_id, organization=org)
    except Lead.DoesNotExist:
        return redirect('leads')
        
    activities = lead.activities.all().order_by('-timestamp')
    tasks = lead.tasks.all().order_by('-created_at')
    
    context = {
        'lead': lead,
        'activities': activities,
        'tasks': tasks
    }
    return render(request, 'contact_detail.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        desc = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority', 'Medium')
        org = request.user.profile.organization
        
        try:
            lead = Lead.objects.get(id=lead_id, organization=org)
            task = Task.objects.create(
                lead=lead,
                description=desc,
                due_date=due_date,
                priority=priority
            )
            # Log activity
            Activity.objects.create(
                lead=lead,
                type='Task',
                description=f"Created task: {desc} (Priority: {priority}, Due: {due_date})"
            )
            return JsonResponse({
                'success': True,
                'task': {
                    'id': task.id,
                    'description': task.description,
                    'due_date_formatted': task.due_date.strftime('%b %d'),
                    'priority': task.priority,
                    'completed': task.completed
                }
            })
        except Lead.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lead not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def complete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        org = request.user.profile.organization
        
        try:
            task = Task.objects.get(id=task_id, lead__organization=org)
            task.completed = not task.completed
            task.save()
            
            # Log activity
            status_text = "completed" if task.completed else "re-opened"
            Activity.objects.create(
                lead=task.lead,
                type='Task',
                description=f"Marked task '{task.description}' as {status_text}."
            )
            return JsonResponse({'success': True, 'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def log_activity(request):
    if request.method == 'POST':
        lead_id = request.POST.get('lead_id')
        act_type = request.POST.get('type')
        desc = request.POST.get('description')
        org = request.user.profile.organization
        
        try:
            lead = Lead.objects.get(id=lead_id, organization=org)
            activity = Activity.objects.create(
                lead=lead,
                type=act_type,
                description=desc
            )
            # Update last activity datetime implicitly through save
            lead.save()
            
            return JsonResponse({
                'success': True,
                'activity': {
                    'type': activity.type,
                    'description': activity.description,
                    'timestamp': activity.timestamp.strftime('%Y-%m-%d %H:%M')
                }
            })
        except Lead.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lead not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def quick_create_lead(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('company')
        value = request.POST.get('value', 0)
        score = request.POST.get('score', 50)
        
        org = request.user.profile.organization
        owner = request.user.profile
        
        try:
            lead = Lead.objects.create(
                organization=org,
                name=name,
                email=email,
                company=company,
                value=value,
                score=score,
                owner=owner,
                status='New',
                stage='New',
                lifecycle_stage='Prospect',
                health_score=80,
                annual_revenue=value
            )
            Activity.objects.create(
                lead=lead,
                type='Creation',
                description="Lead added via quick create."
            )
            messages.success(request, f"Successfully created lead '{name}' for {company}.")
        except Exception as e:
            messages.error(request, f"Error creating lead: {str(e)}")
            
    return redirect(request.META.get('HTTP_REFERER', 'leads'))

@login_required
def calendar_view(request):
    """Display calendar with events for the user's organization."""
    org = request.user.profile.organization
    events = Event.objects.filter(organization=org).order_by('start_time')
    return render(request, 'calendar.html', {'events': events})

@login_required
def event_create_view(request):
    """Create a new calendar event via modal form."""
    org = request.user.profile.organization
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.organization = org
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form, 'action': 'Create'})

@login_required
def event_edit_view(request, event_id):
    """Edit an existing calendar event."""
    org = request.user.profile.organization
    event = get_object_or_404(Event, id=event_id, organization=org)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('calendar')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form, 'action': 'Edit'})

@login_required
def event_delete_view(request, event_id):
    """Delete a calendar event."""
    org = request.user.profile.organization
    event = get_object_or_404(Event, id=event_id, organization=org)
    event.delete()
    messages.success(request, 'Event deleted.')
    return redirect('calendar')

@login_required
def profile_edit_view(request):
    """Edit user profile fields and avatar."""
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        # Handle built‑in User fields separately
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_edit')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form, 'user': user})

@login_required
def upgrade_plans_view(request):
    """Show available billing plans and current subscription."""
    org = request.user.profile.organization
    plans = BillingPlan.objects.all()
    subscription = Subscription.objects.filter(user_profile=request.user.profile).first()
    return render(request, 'upgrade_plans.html', {'plans': plans, 'subscription': subscription})

@login_required
def subscribe_plan_view(request, plan_id):
    """Subscribe the user to a selected plan."""
    org = request.user.profile.organization
    plan = get_object_or_404(BillingPlan, id=plan_id)
    # Simple subscription creation – replace any existing one
    Subscription.objects.update_or_create(
        user_profile=request.user.profile,
        defaults={'plan': plan, 'status': 'active'}
    )
    messages.success(request, f'Subscribed to {plan.name} plan.')
    return redirect('upgrade_plans')

