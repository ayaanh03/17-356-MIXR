from django.urls import path, include
from mixr import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('/', views.hello, name='hello')
    path('joinPrivate.html', views.joinPrivate),
    path('createRoom.html', views.createRoom),
]
