# mini_insta/models.py
# Ting Shing Liu, 9/26/25
# Creating the profile and Post object with fields that will be stored in the database
from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a Profile '''

    # define the data attributes of the Profile object

    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance '''

        return f'{self.display_name} joined {self.join_date}'
    
    def get_all_posts(self):
        '''Return a QuerySet of Posts on this Profile'''
        # Use the object manager to retrieve Posts from this profile
        posts = Post.objects.filter(profile=self).order_by("timestamp")
        return posts
    
class Post(models.Model):
    '''Encapsulate the data of the Post object'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''

        return f'Post for {self.profile}'
    
    def get_all_photos(self):
        '''Return a QuerySet of all Photos on this Post'''
        # Use the object manager to retrieve Photos from this Post
        photos = Photo.objects.filter(post=self).order_by("timestamp")
        return photos
    
class Photo(models.Model):
    '''Encapsulate the data of the Photo object'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''

        return f'Photo for {self.post}'