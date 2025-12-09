# project/forms.py
# Ting Shing Liu, 12/08/25
# Define the forms that we use for create/update/delete operations

from django import forms
from .models import *
from django.contrib.auth.models import User

class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""
    class Meta:
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    """A form to update a Profile in the database"""
    # dob is a DateField, so we add a specific widget for it
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['name', 'dob', 'bio_text', 'profile_image_url']

class CreateProfileForm(forms.ModelForm):
    """A form to create a Profile in the database"""
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['name', 'dob', 'bio_text', 'profile_image_url']

class CreateMessageForm(forms.ModelForm):
    """A form to send a message"""
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Type a message...', 
                'autocomplete': 'off'
            }),
        }
        # Hide the label
        labels = {
            'text': '',
        }