# voter_analytics/urls.py
# Ting Shing Liu, 10/31/25
# URL configuration for Voter Analytics app

from django.urls import path
from . import views 
 
urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'), # maps the base URL to the VoterListView
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'), # maps the URL with voter ID to the VoterDetailView
    path('graphs', views.VoterGraphView.as_view(), name='graphs'), # maps the URL for graphs to the VoterGraphView
]