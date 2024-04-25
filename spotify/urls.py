from django.urls import path
from spotify import views
urlpatterns = [
    path('', views.categories, name='categories'),
    path('search/', views.search, name='search'),
    path('player/<str:url>/', views.player, name='player'),
    path('playlists/<str:url>/', views.playlists, name='playlists')
]
