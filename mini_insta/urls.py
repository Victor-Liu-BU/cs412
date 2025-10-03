# file: mini_insta/urls.py
# Author: Ting Shing Liu, 9/25/25
# Description: The url path page for my mini_insta app 

from django.urls import path
from django.conf import settings
from .views import * # Import All Views from views.py

# URL patterns specific to the mini insta app:
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"), # Path to the base page where it displays all profiles 
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"), # Path to a unique profile page with their respective id 
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"), # Path to a unique post with their respective id 
    path('profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"), # Path to the create post form with their respective profile id
]