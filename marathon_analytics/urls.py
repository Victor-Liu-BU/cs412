# marathon_analytics/urls.py
 
from django.urls import path
from .views import *
 
urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', ResultsListView.as_view(), name='home'),
    path(r'results', ResultsListView.as_view(), name='results_list'),
    path(r'result/<int:pk>', ResultDetailView.as_view(), name='result_detail'),
]