# dadjokes/views.py
# Ting Shing Liu, 11/14/25
# Views for the dad jokes webapp

from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import JokeSerializer, PictureSerializer

class RandomPageView(TemplateView):
    """
    View for '' and 'random'
    """
    template_name = 'dadjokes/random_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['joke'] = Joke.objects.order_by('?').first()
        context['picture'] = Picture.objects.order_by('?').first()
        return context

class JokeListView(ListView):
    """
    View for 'jokes' - shows all Jokes
    """
    model = Joke
    template_name = "dadjokes/all_jokes.html"
    context_object_name = "jokes"
    ordering = ['-timestamp']

class JokeDetailView(DetailView):
    """
    View for 'joke/<int:pk>' - shows one Joke
    """
    model = Joke
    template_name = "dadjokes/single_joke.html"
    context_object_name = "joke"

class PictureListView(ListView):
    """
    View for 'pictures' - shows all Pictures
    """
    model = Picture
    template_name = "dadjokes/all_pictures.html"
    context_object_name = "pictures"
    ordering = ['-timestamp']

class PictureDetailView(DetailView):
    """
    View for 'picture/<int:pk>' - shows one Picture
    """
    model = Picture
    template_name = "dadjokes/single_picture.html"
    context_object_name = "picture"


# --- REST API Class-Based Views (NEW) ---

class JokeListAPIView(generics.ListCreateAPIView):
    '''
    An API view to return a listing of Jokes
    and to create a new Joke. (Handles GET and POST)
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeDetailAPIView(generics.RetrieveAPIView):
    '''
    An API view to return a single Joke. (Handles GET)
    
    Note: We use RetrieveAPIView, not RetrieveUpdateDestroyAPIView,
    because the assignment only requires GET (retrieve).
    '''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    '''
    An API view to return a listing of Pictures. (Handles GET)
    
    Note: We use ListAPIView, not ListCreateAPIView,
    because the assignment only requires GET (list).
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveAPIView):
    '''
    An API view to return a single Picture. (Handles GET)
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


# --- Custom API Function-Based Views (Unchanged) ---
# (Generic views aren't good for "random" logic)

@api_view(['GET'])
def api_random_joke(request):
    """
    View for 'api/' and 'api/random'
    """
    joke = Joke.objects.order_by('?').first()
    if joke:
        serializer = JokeSerializer(joke)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def api_random_picture(request):
    """
    View for 'api/random_picture'
    """
    picture = Picture.objects.order_by('?').first()
    if picture:
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)