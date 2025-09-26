# mini_insta/models.py
# Ting Shing Liu, 9/26/25
# Creating the profile object with fields that will be stored in the database
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