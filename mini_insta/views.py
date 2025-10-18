# mini_insta/views.py
# Ting Shing Liu, 9/26/25
# Views file for the mini_insta app that describes the Profile classes that will be used in the application
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
from django.db.models import Q

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
    
class UpdateProfileView(UpdateView):
    '''A view to handle the update of the Profile object'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    '''A view to handle the deletion of the Post object'''

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        # Calling the superclass method 
        context = super().get_context_data(**kwargs)


        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        """Return a url to return to after a successful deletion"""

        # find the PK for this post:
        pk = self.kwargs['pk']
        # find the Post object:
        post = Post.objects.get(pk=pk)
        
        # find the PK of the profile for which this post is associated to 
        profile = post.profile

        # return the URL to redirect to:
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
class UpdatePostView(UpdateView):
    '''A view to handle the update of a Post object'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class ShowFollowersDetailView(DetailView):
    '''A view to show the followers of a Profile'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''A view to show who a Profile is following'''

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ListView):
    '''A view to show the list of posts of an associated feed'''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """
        This method filters and orders the posts for the feed.
        """
        # Get the profile primary key from the URL
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)

        # Get the list of profiles this user is following
        # (This relies on your Profile.get_following() model method)
        following_profiles = profile.get_following()
        
        # Filter posts to only include those from the followed profiles
        # AND order by timestamp descending (newest first).
        queryset = Post.objects.filter(
            profile__in=following_profiles
        ).order_by('-timestamp') 
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add the profile object to the context so we can display
        the profile's username in the template."""

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Get the profile object using the pk from the URL and add it to the context
        profile_pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=profile_pk)
        
        return context

class SearchView(ListView):
    '''A view to handle searching for posts and profiles'''

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    def dispatch(self, request, *args, **kwargs):
        """
        Overrides the dispatch method.
        If no 'query' is in the GET request, it shows the search.html form.
        Otherwise, it proceeds with the ListView's normal flow.
        """
        query = self.request.GET.get('query')
        if not query:
            # No query submitted, so show the search form
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            context = {'profile': profile}
            return render(request, 'mini_insta/search.html', context)
        
        # A query is present, so let the ListView handle it
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns a queryset of Posts matching the search query.
        A Post matches if the query is in its caption.
        """
        query = self.request.GET.get('query')
        if query:
            # Search Post captions
            return Post.objects.filter(caption__icontains=query)
        
        # Return an empty queryset if no query (though dispatch should prevent this)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        """
        Adds the search query, the searching profile, and
        the Profile search results to the context.
        """
        # Call the base implementation first to get context (which includes 'posts')
        context = super().get_context_data(**kwargs)
        
        query = self.request.GET.get('query')
        profile_pk = self.kwargs['pk']
        
        # Add the searching profile to the context
        context['profile'] = Profile.objects.get(pk=profile_pk)
        
        # Add the query string to the context
        context['query'] = query
        
        return context