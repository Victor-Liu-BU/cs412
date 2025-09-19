# file: restaurant/urls.py
# Author: Ting Shing Liu, 9/16/25
# Description: The url path page for my restaurant app 

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the restaurant app:
urlpatterns = [
    path(r'', views.main, name="main_page"), # Path to the base page which is the same as the main page 
    path(r'main', views.main, name="main_page"), # Path to the Main page
    path(r'order', views.order, name="order_page"), # Path to the Order page 
    path(r'confirmation', views.confirmation, name="confirmation_page"), # Path to the Confirmation Page
]