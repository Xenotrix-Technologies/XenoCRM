from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from crm.models import Organization, UserProfile, Lead, Task, Activity

class XenoCRMTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Org 1
        self.org1 = Organization.objects.create(name="Org One")
        self.user1 = User.objects.create_user(username="user1", password="password123", email="user1@org1.com")
        self.profile1 = UserProfile.objects.create(user=self.user1, organization=self.org1, role="Manager")
        
        # Lead for Org 1
        self.lead1 = Lead.objects.create(
            organization=self.org1,
            name="John Doe",
            email="john@doe.com",
            company="Doe Corp",
            score=90,
            status="New",
            stage="New",
            value=10000,
            owner=self.profile1
        )
        
        # Task for Lead 1
        self.task1 = Task.objects.create(
            lead=self.lead1,
            description="Send quote",
            due_date="2026-10-10",
            priority="High",
            completed=False
        )

        # Org 2
        self.org2 = Organization.objects.create(name="Org Two")
        self.user2 = User.objects.create_user(username="user2", password="password123", email="user2@org2.com")
        self.profile2 = UserProfile.objects.create(user=self.user2, organization=self.org2, role="Representative")
        
        # Lead for Org 2
        self.lead2 = Lead.objects.create(
            organization=self.org2,
            name="Jane Smith",
            email="jane@smith.com",
            company="Smith Ltd",
            score=85,
            status="Contacted",
            stage="Qualified",
            value=25000,
            owner=self.profile2
        )

    def test_signup(self):
        response = self.client.post(reverse('signup'), {
            'org_name': 'Test New Org',
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'testpassword123',
            'password_confirm': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Organization.objects.filter(name='Test New Org').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'user1',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_multi_tenancy(self):
        # Log in user 1
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Context should show org 1's lead but not org 2's lead
        leads = response.context['new_leads']
        self.assertIn(self.lead1, leads)
        self.assertNotIn(self.lead2, leads)
        
        # Total revenue should only sum Org 1's leads in Won stage (currently 0)
        self.assertEqual(response.context['total_revenue'], 0)

    def test_leads_view_multi_tenancy(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('leads'))
        self.assertEqual(response.status_code, 200)
        
        leads = response.context['leads']
        self.assertIn(self.lead1, [l for l in leads])
        self.assertNotIn(self.lead2, [l for l in leads])

    def test_update_lead_stage_ajax(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('update_lead_stage'), {
            'lead_id': self.lead1.id,
            'stage': 'Proposal'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Refresh and assert stage updated
        self.lead1.refresh_from_db()
        self.assertEqual(self.lead1.stage, 'Proposal')
        self.assertTrue(Activity.objects.filter(lead=self.lead1, type='Stage Update').exists())

    def test_complete_task_ajax(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('complete_task'), {
            'task_id': self.task1.id
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['completed'])
        
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

    def test_log_activity_ajax(self):
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('log_activity'), {
            'lead_id': self.lead1.id,
            'type': 'Call',
            'description': 'Discovery call logged.'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['activity']['type'], 'Call')
        self.assertEqual(data['activity']['description'], 'Discovery call logged.')
        
        self.assertTrue(Activity.objects.filter(lead=self.lead1, type='Call', description='Discovery call logged.').exists())

    def test_new_views_require_login(self):
        new_views = [
            'contacts', 'accounts', 'opportunities', 'marketing', 
            'customer_support', 'projects', 'reports', 'ai_assistant', 
            'business', 'campaign'
        ]
        # Test anonymous access redirects to login
        for view_name in new_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse('login'), response.url)

    def test_new_views_authenticated(self):
        new_views = [
            'contacts', 'accounts', 'opportunities', 'marketing', 
            'customer_support', 'projects', 'reports', 'ai_assistant', 
            'business', 'campaign'
        ]
        # Log in user
        self.client.login(username='user1', password='password123')
        for view_name in new_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 200, f"Failed for view {view_name}")
