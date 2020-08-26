from django.contrib import admin
from .models import Face, FaceHist, FaceScore

admin.site.register(Face)
admin.site.register(FaceHist)
admin.site.register(FaceScore)