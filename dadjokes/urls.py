# dadjokes/urls.py
from django.urls import path
from .views import * # Imports all views from views.py

urlpatterns = [
    path('', RandomPageView.as_view(), name='random_page'), # 'random' - random joke/picture
    path('random/', RandomPageView.as_view(), name='random_page_alt'), # 'jokes' - all jokes
    path('jokes/', JokeListView.as_view(), name='all_jokes'), # 'joke/<int:pk>' - one joke
    path('joke/<int:pk>/', JokeDetailView.as_view(), name='single_joke'), # 'pictures' - all pictures
    path('pictures/', PictureListView.as_view(), name='all_pictures'), # 'picture/<int:pk>' - one picture
    path('picture/<int:pk>/', PictureDetailView.as_view(), name='single_picture'),

    # Generic Class-Based API Views
    path('api/jokes/', JokeListAPIView.as_view(), name='api_joke_list'),
    path('api/joke/<int:pk>/', JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures/', PictureListAPIView.as_view(), name='api_picture_list'),
    path('api/picture/<int:pk>/', PictureDetailAPIView.as_view(), name='api_picture_detail'),
    
    # Custom Function-Based API Views (for random)
    path('api/', api_random_joke, name='api_random_joke'),
    path('api/random/', api_random_joke, name='api_random_joke_alt'),
    path('api/random_picture/', api_random_picture, name='api_random_picture'),
]