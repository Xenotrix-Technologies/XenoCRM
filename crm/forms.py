from django import forms
from django.contrib.auth.models import User
from .models import Event, UserProfile


class EventForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary'
            }
        )
    )
    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M'],
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'datetime-local',
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary'
            }
        )
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'recurring', 'color']

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
            'recurring': forms.CheckboxInput(attrs={
                'class': 'rounded border-outline-variant text-primary focus:ring-primary h-4 w-4'
            }),
            'color': forms.Select(
                choices=[
                    ('#004ac6', 'Meeting (Blue)'),
                    ('#10b981', 'Demo (Green)'),
                    ('#ef4444', 'Deadline (Red)'),
                    ('#8b5cf6', 'Follow-up (Purple)'),
                    ('#f97316', 'Personal (Orange)'),
                ],
                attrs={
                    'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary'
                }
            )
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image_url', 'phone_number', 'location', 'role']
        widgets = {
            'profile_image_url': forms.URLInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary',
                'placeholder': 'https://example.com/avatar.jpg'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary',
                'placeholder': '+1 (555) 000-0000'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary',
                'placeholder': 'e.g. New York, USA'
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-body-sm focus:ring-1 focus:ring-primary focus:border-primary opacity-70 cursor-not-allowed',
                'placeholder': 'e.g. Sales Director',
                'readonly': 'readonly'
            })
        }

    # username, first_name, last_name, email are on User model, handle separately in view
