from django.urls import path
from . import views

app_name = 'scp'

urlpatterns = [
    path('', views.register, name='registerUser'),
    path('home/', views.HomePageView.as_view(), name='home-page'),
]