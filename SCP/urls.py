from django.urls import path
from . import views

urlpatterns = [
    path('', views.LogIn.as_view()),
    path('home/', views.HomePageView.as_view(), name='index'),
]