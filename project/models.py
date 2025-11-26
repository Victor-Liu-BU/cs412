# project/models.py
# Ting Shing Liu, 11/25/25
from django.db import models
from django.urls import reverse 
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Encapsulate the data of a Profile '''
    # Changed name to CharField (better for short text than TextField)
    name = models.CharField(max_length=200, blank=True)
    dob = models.DateField(blank=True, null=True)
    profile_image_url = models.ImageField(upload_to='profiles/', blank=True)
    bio_text = models.TextField(blank=True)
    # We add related_name="project_profiles" to distinguish it from mini_insta
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_profiles")

    def __str__(self):
        '''return a string representation of this model instance '''
        # FIX: Changed to use 'name' and 'user.username'
        # Previous code referenced non-existent fields display_name/join_date
        return f'{self.name} ({self.user.username})'
    
    def get_all_posts(self):
        '''Return a QuerySet of Posts on this Profile'''
        posts = Post.objects.filter(profile=self).order_by("timestamp")
        return posts
    
    def get_absolute_url(self):
        '''Return a url to display one instance of this Profile'''
        return reverse("show_profile", kwargs={'pk':self.pk})

class Post(models.Model):
    '''Encapsulate the data of the Post object'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post for {self.profile}'
    
    def get_all_photos(self):
        '''Return a QuerySet of all Photos on this Post'''
        photos = Photo.objects.filter(post=self).order_by("timestamp")
        return photos
    
    def get_absolute_url(self):
        return reverse("show_post", kwargs={'pk':self.pk})
    
class Photo(models.Model):
    '''Encapsulate the data of the Photo object'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='photos/', blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.image_file:
            return f'Photo from file for {self.post}'
        return f'Photo (no image) for {self.post}'
    
    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        return ''        

class Match(models.Model):
    '''Encapsulate the data of a Match object'''
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    status = models.BooleanField(default=False) # False=Pending, True=Matched
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Match between {self.profile1} and {self.profile2}'
    
class Message(models.Model):
    '''Encapsulate the data of a Message object'''
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    # Added related_name='sender' for symmetry and to avoid collisions
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Message from {self.sender} at {self.timestamp}'
    
class Advice(models.Model):
    '''Encapsulate the data of an Advice object'''
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text[:20]}... by {self.author}'