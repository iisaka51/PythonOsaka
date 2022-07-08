from django.shortcuts import render

from django.http import HttpResponse
from .forms import UserForm


def myview(request):
     return HttpResponse('Hello World')

def index(request):
     values = {
         'title': 'Hello Django',
         'name': ''
     }
     return render(request, 'index.html', values)

def login(request):
     form = UserForm()
     return render(request, 'login.html', {
         'form': form,
     })

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
