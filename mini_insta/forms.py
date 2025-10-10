# mini_insta/forms.py
# Ting Shing Liu, 10/3/25
# Define the forms that we use for create/update/delete operations 

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""

    class Meta:
        """Associate this form with a model in the database"""
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    """A form to update a Profile in the database"""

    class Meta:
        """Associate this form with a model in the database"""
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']