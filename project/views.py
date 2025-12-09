# project/views.py
# Ting Shing Liu, 12/08/25
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo, Match, Message, Advice
from .forms import CreatePostForm, UpdateProfileForm, CreateProfileForm, CreateMessageForm
from django.urls import reverse 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.db.models import Q

# --- Profile Views ---

class ProfileListView(ListView):
    '''View to display a list of all Profiles (The "Browse" page)'''
    model = Profile
    template_name = 'project/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        # Exclude the current user from the list if they are logged in
        if self.request.user.is_authenticated:
            return Profile.objects.exclude(user=self.request.user)
        return Profile.objects.all()

class ProfileDetailView(DetailView):
    '''View to display a single Profile details'''
    model = Profile
    template_name = 'project/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                viewer = Profile.objects.get(user=self.request.user)
                context['viewer_profile'] = viewer
                
                # Check for ANY match record between these two
                match = Match.objects.filter(
                    (Q(profile1=viewer) & Q(profile2=self.object)) | 
                    (Q(profile1=self.object) & Q(profile2=viewer))
                ).first()
                
                context['match'] = match
                
                # Helper logic for the template:
                # Did *I* start this request?
                if match and match.profile1 == viewer:
                    context['i_am_sender'] = True
                else:
                    context['i_am_sender'] = False
                
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        return context

class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile'''
    form_class = CreateProfileForm
    template_name = 'project/create_profile_form.html'

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            context = self.get_context_data()
            context['user_form'] = user_form
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def get_success_url(self):
        return reverse('profile_list')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to handle the update of the Profile object'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'project/update_profile_form.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})

# --- Post & Photo Views ---

class PostListView(LoginRequiredMixin, ListView):
    '''Show a public feed of posts'''
    model = Post
    template_name = 'project/post_list.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']

class PostDetailView(DetailView):
    '''Show a single post with details'''
    model = Post
    template_name = "project/post_detail.html"
    context_object_name = "post"

class CreatePostView(LoginRequiredMixin, CreateView):
    '''Create a new Post and handle multiple Photo uploads'''
    form_class = CreatePostForm
    template_name = 'project/create_post_form.html'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        response = super().form_valid(form)

        image_files = self.request.FILES.getlist('image_files')
        for image in image_files:
            Photo.objects.create(
                post=self.object,
                image_file=image
            )
        return response
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''View to allow a user to update their own post caption'''
    model = Post
    form_class = CreatePostForm # We can reuse the Create form since it just has 'caption'
    template_name = 'project/update_post_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Security Check: 
        Get the post object and verify that the logged-in user 
        is the owner of the profile associated with this post.
        """
        post = self.get_object()
        
        # If the user is trying to edit someone else's post, redirect them away
        if post.profile.user != self.request.user:
            return redirect('show_post', pk=post.pk)
            
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Return to the post detail page after saving"""
        return reverse('show_post', kwargs={'pk': self.object.pk})

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "project/delete_post_form.html"

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

# --- Match & Message Views ---

class CreateMatchView(LoginRequiredMixin, View):
    '''Logic to create a Match request OR Accept an existing one.'''
    def post(self, request, pk):
        profile_to_match = Profile.objects.get(pk=pk) # The person I am looking at
        my_profile = Profile.objects.get(user=request.user) # Me

        if profile_to_match != my_profile:
            # Check if a match record exists
            existing_match = Match.objects.filter(
                (Q(profile1=my_profile) & Q(profile2=profile_to_match)) | 
                (Q(profile1=profile_to_match) & Q(profile2=my_profile))
            ).first()

            if not existing_match:
                # FIX 2: Create as FALSE (Pending). Not True.
                Match.objects.create(
                    profile1=my_profile, # Initiator
                    profile2=profile_to_match, # Receiver
                    status=False # Pending
                )
            elif existing_match.profile2 == my_profile and existing_match.status == False:
                # FIX 2 (Continued): If they asked me, AND I click accept -> Set True
                existing_match.status = True 
                existing_match.save()
            
        return redirect('show_profile', pk=pk)

class DeclineMatchView(LoginRequiredMixin, View):
    '''Logic to delete a pending match request'''
    def post(self, request, pk):
        other_profile = Profile.objects.get(pk=pk)
        my_profile = Profile.objects.get(user=request.user)

        match = Match.objects.filter(
            profile1=other_profile,
            profile2=my_profile,
            status=False
        ).first()

        if match:
            match.delete() 
            
        return redirect('show_profile', pk=pk)

class MatchRequestsListView(LoginRequiredMixin, ListView):
    '''Show incoming connection requests'''
    model = Match
    template_name = 'project/match_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        my_profile = Profile.objects.get(user=self.request.user)
        # Find matches where I am the receiver (profile2) and status is False
        return Match.objects.filter(profile2=my_profile, status=False)

class ConversationView(LoginRequiredMixin, View):
    '''Display messages in a match and handle sending new messages'''
    template_name = 'project/conversation.html'

    def get(self, request, pk):
        match = Match.objects.get(pk=pk)
        
        # FIX 1: Define user_profile so we can use it in context
        user_profile = Profile.objects.get(user=request.user)

        # Security check: Ensure status is True
        if not match.status:
            return redirect('profile_list')

        messages = Message.objects.filter(match=match).order_by('timestamp')
        form = CreateMessageForm()
        context = {
            'match': match,
            'messages': messages,
            'form': form,
            'my_profile': user_profile # Now this variable exists!
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        match = Match.objects.get(pk=pk)
        user_profile = Profile.objects.get(user=request.user)
        
        # Determine receiver
        if user_profile == match.profile1:
            receiver = match.profile2
        else:
            receiver = match.profile1

        form = CreateMessageForm(request.POST)
        if form.is_valid():
            form.instance.match = match
            form.instance.sender = user_profile
            form.instance.receiver = receiver
            form.save()
        return redirect('show_conversation', pk=pk)

# --- Advice Views ---

class AdviceListView(ListView):
    '''Display generic dating advice'''
    model = Advice
    template_name = 'project/advice_list.html'
    context_object_name = 'advice_list'