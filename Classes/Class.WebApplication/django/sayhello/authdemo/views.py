from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import UserForm
from urllib.parse import urlencode


def myview(request):
     return HttpResponse('Hello World')

def login(request):
      if request.method == 'POST':
           redirect_url = reverse('authdemo:index')
           parameters = urlencode({'name': request.POST.get('name')})
           url = f'{redirect_url}?{parameters}'
           return redirect(url)
      else:
           form = UserForm()
           values = { 'form': form }
           return render(request, 'login.html', values)

def index(request):
       values = {'name': request.GET.get('name') }
       return render(request, 'index.html', values)

def artist_list(request):
     values={
        'artist_list': [ {
           'firstname': 'Freddie',
           'lastname': 'Mercury',
           'born_place': 'Farrokh Bulsara',
           'born_date': '1946-9-5'
        },
        {
           'firstname': 'David',
           'lastname': 'Bowie',
           'born_place': 'Brixton, London, England',
           'born_date': '1947-1-8'
        },
      ]
     }
     return render(request, 'artist_list.html', values)
