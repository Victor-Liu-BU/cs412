# project/urls.py
# Ting Shing Liu, 12/08/25
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- Profile URLs ---
    path('', views.ProfileListView.as_view(), name='profile_list'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='show_profile'),
    path('profile/create/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    
    # --- Match & Requests ---
    path('profile/<int:pk>/match/', views.CreateMatchView.as_view(), name='create_match'),
    path('profile/<int:pk>/decline/', views.DeclineMatchView.as_view(), name='decline_match'),
    path('requests/', views.MatchRequestsListView.as_view(), name='match_requests'),
    
    # --- Post URLs ---
    path('feed/', views.PostListView.as_view(), name='show_feed'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='show_post'),
    path('post/create/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),

    # --- Message URLs ---
    path('match/<int:pk>/messages/', views.ConversationView.as_view(), name='show_conversation'),

    # --- Advice URLs ---
    path('advice/', views.AdviceListView.as_view(), name='show_advice'),

    # --- Auth URLs ---
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='profile_list'), name='logout'),
]