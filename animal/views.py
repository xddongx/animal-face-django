from django.shortcuts import render
from django.views.generic import ListView
from face.models import Face

# def index(request):
#     return render(request, 'animal/index.html')


class index(ListView):
    model = Face

