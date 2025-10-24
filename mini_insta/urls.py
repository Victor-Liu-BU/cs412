# file: mini_insta/urls.py
# Author: Ting Shing Liu, 9/25/25
# Description: The url path page for my mini_insta app 

from django.urls import path
from django.conf import settings
from .views import * # Import All Views from views.py
from django.contrib.auth import views as auth_views

# URL patterns specific to the mini insta app:
urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"), # Path to the base page where it displays all profiles 
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"), # Path to a unique profile page with their respective id 
    path('profile/', ProfileDetailView.as_view(), name="show_my_profile"), # Path to the user's own profile page
    path('post/<int:pk>', PostDetailView.as_view(), name="show_post"), # Path to a unique post with their respective id 
    path('profile/create_post', CreatePostView.as_view(), name="create_post"), # Path to the create post form with their respective profile id
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"), # Path to the update profile form with their respective profile id
    path('post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"), # Path that would lead to the profile of the post that was deleted with their respective post id
    path('post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"), # Path to the update Post form with their respective post id 
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'), # Path to the followers page
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'), # Path to the following page
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'), # Path to the feed page of profiles followed by the user
    path('profile/search', SearchView.as_view(), name='search'), # Path to the search page
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'), # Path to the login page
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'), # Path to the logout page
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'), # Path to the create profile page
    path('profile/<int:pk>/follow', AddFollowView.as_view(), name='follow'), # Path to follow a profile
    path('profile/<int:pk>/delete_follow', RemoveFollowView.as_view(), name='unfollow'), # Path to unfollow a profile
    path('post/<int:pk>/like', AddLikeView.as_view(), name='like_post'), # Path to like a post
    path('post/<int:pk>/delete_like', RemoveLikeView.as_view(), name='unlike_post'), # Path to unlike a post
]