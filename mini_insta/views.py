# mini_insta/views.py
# Ting Shing Liu, 9/26/25
# Views file for the mini_insta app that describes the Profile classes that will be used in the application
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    '''Define a class inherited from ListView to show all Profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Define a class inherited from DetailView to show a single Profile with details'''
    
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"