# mini_insta/models.py
# Ting Shing Liu, 9/26/25
# Creating the profile and Post object with fields that will be stored in the database
from django.db import models
from django.urls import reverse 

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
    
    def get_absolute_url(self):
        '''Return a url to display one instance of this Profile'''
        return reverse("show_profile", kwargs={'pk':self.pk})
    
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
    
    def get_absolute_url(self):
        """Return a URL to display one instance of this object """
        return reverse("show_post", kwargs={'pk':self.pk})
    
class Photo(models.Model):
    '''Encapsulate the data of the Photo object'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''
        if self.image_url:
            return f'Photo from URL for {self.post}'
        elif self.image_file:
            return f'Photo from file for {self.post}'
        return f'Photo (no image) for {self.post}'
    
    def get_image_url(self):
        '''Return a url from either image_url or image_file'''
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        # Return an empty string if no image source is available
        return ''        
        
            