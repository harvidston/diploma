from django.urls import path

from publications.views import user_views as views

from rest_framework_simplejwt.views import (
        TokenRefreshView,
)

urlpatterns = [


        path('', views.getUsers, name='all_users'),
        path('name/', views.getUserUsername, name='username'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('profile/', views.getUserSettings, name='users_settings'),


        path('profile/update/', views.updateUserSettings, name='user_settings_update'),

        path('artist/upload/', views.uploadArtistImage, name='artist_image_upload'),
        

        path('register/', views.registerUser, name = 'register_user'),

        path('info/<str:pk>/', views.getUserProfile, name = 'user_profile_info'),

        path('publicationsamount/<str:pk>/', views.getUserPublicationsAmount, name = 'user_profile_info'),

        path('artists/', views.getArtists, name = 'artists'),

        path('artist/follow/<int:pk>/', views.followArtist, name = 'artist_follow'),
        path('artist/unfollow/<int:pk>/', views.unfollowArtist, name = 'artist_unfollow'),
        path('artist/followers/<int:pk>', views.getFollowersArtist, name = 'artist_followers'),
        path('artist/following/<int:pk>', views.getFollowingArtist, name = 'artist_following'),

        path('artist/<str:pk>/', views.getArtist, name = 'artist_image'),
        path('artist/update/', views.updateArtistDetails, name='artist_details_update'),



]
