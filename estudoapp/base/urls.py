from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('sala/<str:pk>/', views.sala, name='sala'),

    path('profile/<str:pk>/', views.user_profile, name='user_profile'),

    path('create_sala/', views.create_sala, name='create_sala'),
    path('update_sala/<str:pk>', views.update_sala, name='update_sala'),
    path('delete_sala/<str:pk>', views.delete_sala, name='delete_sala'),

    path('delete_message/<str:pk>', views.delete_message, name='delete_message'),

    path('update_user/', views.update_user, name='update_user'),

    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]