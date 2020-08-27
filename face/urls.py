"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name='face'
urlpatterns = [
    path('', views.FaceCV, name='create'),
    path('facehist/<int:pk>', views.FaceDV.as_view(), name='detail'),
    # path('facehist/<int:pk>', views.FaceDV, name='detail'),
    path('facehist/modal/', views.FaceModal, name='modal'),
    path('facehist/<int:pk>/screenshot', views.Screenshot, name='screenshot'),
    path('screen/', views.generate_PDF),
    # path('test/', views.graph),
]

