from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormView
from .models import Face, FaceHist
from .forms import FaceForm
from django.urls import reverse_lazy

# class FaceCV(CreateView):
#     form_class = FaceForm
#     template_name = 'face/face.html'

#     def form_valid(self, form):
#         if form.is_valid():
#             age = form.instance.age
#             gender = form.instance.gender
#             image = form.instance.image
#             message = '정상처리'
#             face_id = Face.objects.get(pk=2)
#             FaceHist.save(message=message, face=face_id)
#             return super().form_valid(form)
#         return super(FaceCV, self).form_valid(form)

def FaceCV(request):
    # faceHist = FaceHist.objects.all()
    # context = {'faceHist':faceHist}
    message = '정상처리'
    face_id = Face.objects.get(pk=2)
    
    if request.method == 'POST':
        form = request.POST
        
        facehist_form = FaceHist()
        
        facehist_form.age = form['age_field']
        facehist_form.gender = form['gender_field']
        print(form)
        facehist_form.image = request.FILES['image_field']
        facehist_form.message = message
        facehist_form.face = face_id
        
        facehist_form.save()

        context['face'] = face_id


        return redirect(facehist_form.get_absolute_url(), context)
    else:
        return render(request, 'face/face.html')


class FaceDV(DetailView):
    model = FaceHist
