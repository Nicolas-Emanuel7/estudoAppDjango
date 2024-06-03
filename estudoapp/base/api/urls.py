from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_route),
    path('rooms/', views.get_room),
    path('rooms/<str:pk>', views.get_room_unica),
]