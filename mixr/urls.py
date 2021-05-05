from django.urls import path, include
from mixr import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    # path('/', views.hello, name='hello')
    path('joinPrivate/', views.joinPrivate),
    path('createRoom/', views.createRoom),
    path('Room/<str:code>/', views.Room),
    path('search/<str:query>/', views.search),
    path('Playlist/', views.Playlist),
    # path('createRoom/Playlist/', views.Playlist)
]
