# mini_insta/views.py
# Ting Shing Liu, 9/26/25
# Views file for the mini_insta app that describes the Profile classes that will be used in the application
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.shortcuts import redirect
from django.urls import reverse 
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login ## NEW
from django.views import View

# Create your views here.
class ProfileListView(ListView):
    '''Define a class inherited from ListView to show all Profiles'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(DetailView):
    '''Define a class inherited from DetailView to show a single Profile with details'''
    
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        '''Override get_object to obtain the Profile for the logged-in user'''

        if 'pk' not in self.kwargs:
            user = self.request.user
            profile = Profile.objects.get(user=user)
            return profile
        else:
            return super().get_object()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add the logged-in user's profile to the context, if they exist
        if self.request.user.is_authenticated:
            try:
                viewer_profile = Profile.objects.get(user=self.request.user)
                context['viewer_profile'] = viewer_profile
            except Profile.DoesNotExist:
                context['viewer_profile'] = None # Handle case where user has no profile yet
        else:
             context['viewer_profile'] = None

        return context
class PostDetailView(DetailView):
    '''Define a class interited from DetailView to show a single post with details'''

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Add the logged-in user's profile to the context, if they exist
        if self.request.user.is_authenticated:
            try:
                viewer_profile = Profile.objects.get(user=self.request.user)
                context['viewer_profile'] = viewer_profile
            except Profile.DoesNotExist:
                context['viewer_profile'] = None # Handle case where user has no profile yet
        else:
             context['viewer_profile'] = None

        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Post on a Profile '''
    
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
        
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def get_context_data(self):
        # Calling the superclass method 
        context = super().get_context_data()
        
        # find/add profile to the context data
        # Get the profile for the currently logged-in user
        context['profile'] = Profile.objects.get(user=self.request.user)

        return context
    
    def form_valid(self, form):
        """This method handles the form submission and saves the new object 
        to the Django database.
        We need to add the foreign key (of the Profile) to the Comment
        object before saving it to the database."""

        # Get the profile for the currently logged-in user
        profile = Profile.objects.get(user=self.request.user)

        # Attach this post to the Profile
        form.instance.profile = profile # Set the Foreign Key

        user = self.request.user
        # attach user to form instance (Profile object):
        form.instance.user = user

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
    
    def get_object(self):
        '''Override get_object to obtain the Profile for the logged-in user'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to handle the update of the Profile object'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        """This method handles the form submission and saves the updated
        Profile object to the Django database."""

        user = self.request.user
        # attach user to form instance (Profile object):
        form.instance.user = user

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_object(self):
        '''Override get_object to obtain the Profile for the logged-in user'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    
class DeletePostView(LoginRequiredMixin, DeleteView):
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
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''A view to handle the update of a Post object'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        """This method handles the form submission and saves the updated
        Profile object to the Django database."""

        user = self.request.user
        # attach user to form instance (Profile object):
        form.instance.user = user

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

    def get_object(self):
        '''Override get_object to obtain the Profile for the logged-in user'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    

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

class PostFeedListView(LoginRequiredMixin, ListView):
    '''A view to show the list of posts of an associated feed'''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """
        This method returns the queryset of posts for the feed of the logged-in user.
        """
        # Get the profile for the currently logged-in user
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        """Add the profile object to the context so we can display
        the profile's username in the template."""

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Get the profile for the currently logged-in user
        context['profile'] = Profile.objects.get(user=self.request.user)
        
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        """This method handles the form submission and saves the updated
        Profile object to the Django database."""

        user = self.request.user
        # attach user to form instance (Profile object):
        form.instance.user = user

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

    def get_object(self):
        '''Override get_object to obtain the Profile for the logged-in user'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

class SearchView(LoginRequiredMixin, ListView):
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
            # Get the profile for the currently logged-in user
            profile = Profile.objects.get(user=self.request.user)
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

        # Get the profile for the currently logged-in user
        context['profile'] = Profile.objects.get(user=self.request.user)
        
        # Add the query string to the context
        context['query'] = query
        
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        """This method handles the form submission and saves the updated
        Profile object to the Django database."""

        user = self.request.user
        # attach user to form instance (Profile object):
        form.instance.user = user

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

    def get_object(self):
        '''Override get_object to obtain the Profile for the logged-in user'''
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    
class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile in the database'''
    
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
        
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

    def form_valid(self, form):
        '''Handle the form submission to create a new User and Profile object.'''
        
        # Reconstruct the UserCreationForm from the POST data
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # Save the new User object
            user = user_form.save()

            # Log the new user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Attach the new user to the Profile form instance
            form.instance.user = user

            # Delegate the rest to the super class' form_valid (saves profile, redirects)
            return super().form_valid(form)
        else:
            # The UserCreationForm was invalid, so re-render the page
            # with both forms and their errors.
            context = self.get_context_data()
            context['form'] = form           # The (valid) CreateProfileForm
            context['user_form'] = user_form # The (invalid) UserCreationForm
            return self.render_to_response(context)
        
    def get_context_data(self, **kwargs):
        # Calling the superclass method 
        context = super().get_context_data(**kwargs)
        
        # Add an instance of the UserCreationForm to the context
        context['user_form'] = UserCreationForm()

        return context
    
class AddFollowView(LoginRequiredMixin, View):
    '''A view to handle the creation of a Follow object'''
    
    def get_login_url(self):
        return reverse('login')

    def post(self, request, *args, **kwargs):
        # Get the profile to follow (the "other" profile)
        profile_to_follow_pk = self.kwargs['pk']
        profile_to_follow = Profile.objects.get(pk=profile_to_follow_pk)

        # Get the current user's profile (the "follower")
        follower_profile = Profile.objects.get(user=request.user)

        # Check constraint: Don't allow following yourself
        if profile_to_follow != follower_profile:
            # Create the Follow object, if it doesn't already exist
            Follow.objects.get_or_create(
                profile=profile_to_follow,
                follower_profile=follower_profile
            )

        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_follow_pk)

class RemoveFollowView(LoginRequiredMixin, View):
    '''A view to handle the deletion of a Follow object'''
    
    def get_login_url(self):
        return reverse('login')

    def post(self, request, *args, **kwargs):
        # Get the profile to unfollow
        profile_to_unfollow_pk = self.kwargs['pk']
        profile_to_unfollow = Profile.objects.get(pk=profile_to_unfollow_pk)

        # Get the current user's profile
        follower_profile = Profile.objects.get(user=request.user)

        # Find and delete the Follow object
        follow_instance = Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=follower_profile
        )
        if follow_instance.exists():
            follow_instance.delete()

        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_unfollow_pk)

class AddLikeView(LoginRequiredMixin, View):
    '''A view to handle the creation of a Like object'''
    
    def get_login_url(self):
        return reverse('login')

    def post(self, request, *args, **kwargs):
        # Get the post to like
        post_pk = self.kwargs['pk']
        post_to_like = Post.objects.get(pk=post_pk)

        # Get the current user's profile (the "liker")
        liker_profile = Profile.objects.get(user=request.user)

        # Check constraint: Don't allow liking your own post
        if post_to_like.profile != liker_profile:
            # Create the Like object, if it doesn't already exist
            Like.objects.get_or_create(
                post=post_to_like,
                profile=liker_profile
            )

        # Redirect back to the post page
        return redirect('show_post', pk=post_pk)

class RemoveLikeView(LoginRequiredMixin, View):
    '''A view to handle the deletion of a Like object'''
    
    def get_login_url(self):
        return reverse('login')

    def post(self, request, *args, **kwargs):
        # Get the post to unlike
        post_pk = self.kwargs['pk']
        post_to_unlike = Post.objects.get(pk=post_pk)

        # Get the current user's profile
        liker_profile = Profile.objects.get(user=request.user)

        # Find and delete the Like object
        like_instance = Like.objects.filter(
            post=post_to_unlike,
            profile=liker_profile
        )
        if like_instance.exists():
            like_instance.delete()

        # Redirect back to the post page
        return redirect('show_post', pk=post_pk)