from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('mainpage', views.mainpage, name="mainpage"),
    path('movie/<int:movie_id>/', views.movie_detail, name="movie"),
    path('book_ticket/<int:movie_id>/', views.book_ticket, name="book_ticket"),

]