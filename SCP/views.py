from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import CustomUserCreationForm
from django.contrib import messages

from django.views.generic import TemplateView, CreateView

# Create your views here.

# def index(request):
#     return render(request, 'SCP/index.html')


def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('scp:home-page')

        # if not form.is_valid():
        #     return redirect('scp:home-page')
    else:
        form = CustomUserCreationForm()
        context = {'form':form}

        return render(request, 'SCP/login.html', context) 



# class LogIn(TemplateView):
#     template_name = 'SCP/login.html'



class HomePageView(TemplateView):
    template_name = 'SCP/index.html'




