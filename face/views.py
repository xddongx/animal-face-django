from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from .models import Face, FaceHist
from .forms import FaceForm

class FaceCV(CreateView):
    form_class = FaceForm
    template_name = 'face/face.html'

    def form_valid(self, form):
        if form.is_valid():
            age = form.instance.age
            gender = form.instance.gender
            image = form.instance.image
            data = {
                'age' : age,
                'gender' : gender,
                'image': image,
                # 'message': message,
                # 'face': face_id
            }
            print(data)
            return super().form_valid(form)
        return super(FaceCV, self).form_valid(form)

class FaceDV(DetailView):
    model = FaceHist
