# Create your views here.
# project/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile, Post

class ProfileListView(ListView):
    '''View to display a list of all Profiles'''
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''View to display a single Profile details'''
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'