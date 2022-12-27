from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import TemplateView

# Create your views here.

# def index(request):
#     return render(request, 'SCP/index.html')

class LogIn(TemplateView):
    template_name = 'SCP/login.html'



class HomePageView(TemplateView):
    template_name = 'SCP/index.html'