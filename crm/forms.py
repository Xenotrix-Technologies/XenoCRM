from django import forms
from django.contrib.auth.models import User
from .models import Event, UserProfile


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'recurring']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary',
                'placeholder': 'Event Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary',
                'placeholder': 'Event description...',
                'rows': 3
            }),
            'start_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary'
                }
            ),
            'end_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary'
                }
            ),
            'recurring': forms.CheckboxInput(attrs={
                'class': 'rounded border-outline-variant text-primary focus:ring-primary h-4 w-4'
            }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image_url']
        widgets = {
            'profile_image_url': forms.URLInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary',
                'placeholder': 'https://example.com/avatar.jpg'
            })
        }

    # username, first_name, last_name, email are on User model, handle separately in view
