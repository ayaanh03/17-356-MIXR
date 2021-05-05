from django.urls import path, include
from mixr import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    # path('/', views.hello, name='hello')
    path('joinPrivate/', views.joinPrivate),
    path('createRoom.html', views.createRoom),
    path('Room/<str:code>/',views.Room),
    path('search/<str:code>/<str:query>/',views.search),
    path('add/<str:code>/<str:song>/',views.addsong),
    path('getsongs/<str:code>/',views.getsongs),
]
