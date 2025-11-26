# project/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # Map the root URL of the app to the Profile List View
    path('', views.ProfileListView.as_view(), name='profile_list'),
    
    # Map a specific profile ID (pk) to the Detail View
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
]