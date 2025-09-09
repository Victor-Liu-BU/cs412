# file: quotes/urls.py
# Author: Ting Shing Liu, 9/9/25
# Description: urls file for my quotes page

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the hw app:
urlpatterns = [
    path(r'', views.quote, name="quote_page"), # Path to the main page which displays the same thing as the quote page
    path(r'quote', views.quote, name="quote_page"), # Path to the quote page
    path(r'about', views.about, name="about_page"), # Path to the About page 
    path(r'show_all', views.show_all, name="show_all_page"), # Path to the Show_all page which displays all quotes and images
]
