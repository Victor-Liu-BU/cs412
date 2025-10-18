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
    
    def get_followers(self):
        '''Return a list of profiles that follow this profile'''
        followers = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in followers]

    def get_num_followers(self):
        '''Return the number of followers'''
        return len(self.get_followers())

    def get_following(self):
        '''Return a list of profiles that this profile follows'''
        following = Follow.objects.filter(follower_profile=self)
        return [follow.profile for follow in following]

    def get_num_following(self):
        '''Return the number of profiles this profile follows'''
        return len(self.get_following())
    
    def get_post_feed(self):
        '''Return a QuerySet of posts from profiles this user follows'''
        following_profiles = self.get_following()
        # Filter posts to include only those from the profiles the user is following
        # Order by timestamp descending to get the most recent posts first
        post_feed = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        return post_feed
    
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
    
    def get_all_comments(self):
        '''Return a QuerySet of all Comments associated with this Post'''
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_likes(self):
        '''Return a QuerySet of all Likes on this Post'''
        likes = Like.objects.filter(post=self)
        return likes
    
class Photo(models.Model):
    '''Encapsulate the data of the Photo object'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this model instance'''
        # if image_url exist display image_url text else search for image_file 
        # If neither exists, display no image text
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
        
class Follow(models.Model):
    '''Encapsulates the data of the Follow object'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.follower_profile.display_name} follows {self.profile.display_name}'
    
class Comment(models.Model):
    '''Encapsulates the data of the Comment object'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'{self.profile.username} commented {self.text}'
    
class Like(models.Model):
    '''Encapsulates the data of the Like object'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance'''
        return f'Liked by {self.profile.display_name} and {self.post.get_likes().count()} others'