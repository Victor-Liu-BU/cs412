# mini_insta/views.py
# Ting Shing Liu, 9/26/25
# Views file for the mini_insta app that describes the Profile classes that will be used in the application
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm
from django.urls import reverse

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

class PostDetailView(DetailView):
    '''Define a class interited from DetailView to show a single post with details'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    '''A view to handle creation of a new Post on a Profile '''
    
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_context_data(self):
        # Calling the superclass method 
        context = super().get_context_data()
        
        # find/add profile to the context data
        # Retrieve the pk from the URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # Add this profile to the context dictionary
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """This method handles the form submission and saves the new object 
        to the Django database.
        We need to add the foreign key (of the Profile) to the Comment
        object before saving it to the database."""

        # Retrieve the pk from the URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # Attach this post to the Profile
        form.instance.profile = profile # Set the Foreign Key

        # Delegate the work to the superclass method form_valid:
        response = super().form_valid(form)

        # Retrieve the image_url from the POST data
        # image_url = self.request.POST.get('image_url')

        # Retrieve the image files 
        image_files = self.request.FILES.getlist('image_files')

        # Loop through each uploaded file and create a Photo object
        for image in image_files:
            Photo.objects.create(
                post=self.object,
                image_file=image
            )

        # If an image_url was provided, create a new Photo object
        # if image_url:
        #    Photo.objects.create(
        #        post=self.object,
        #        image_url=image_url
        #    )
        # return response
        return response
    