from django.db import models

# Create your models here.
class Joke(models.Model):
    '''Encapsulate the data of a joke'''

    # define the data attributes of the Joke object

    text = models.TextField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance '''

        return f'{self.text}'
    
class Picture(models.Model):
    '''Encapsulate the data of a picture'''

    # define the data attributes of the Picture object

    image_url = models.URLField(blank=False)
    name = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance '''

        return f'{self.name}'