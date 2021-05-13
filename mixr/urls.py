from django.urls import path, include
from mixr import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    # path('/', views.hello, name='hello')
    path('joinPrivate/', views.joinPrivate),
    path('createRoom/', views.createRoom),
    path('Room/<str:code>/<str:host>',views.Room),
    path('search/<str:code>/<str:query>/',views.search),
    path('add/<str:code>/<str:song>/',views.addsong),
    path('getsongs/<str:code>/<int:host>',views.getsongs),
    path('Playlist/', views.Playlist),
    path('update_playlist/<str:code>/<str:song>/<str:up_or_down>/<int:host>', views.update_playlist)
    # path('createRoom/Playlist/', views.Playlist)
]
