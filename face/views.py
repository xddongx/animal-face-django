from django.shortcuts import render, HttpResponseRedirect, redirect
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

# def FaceCV(self, request):
#     # faceHist = FaceHist.objects.all()
#     # context = {'faceHist':faceHist}
#     message = '정상처리'
#     face_id = Face.objects.get(pk=2)
#     if request.method == 'POST':
#         facehist_form = FaceForm(request.POST)
#         if facehist_form.is_valid():
#             facehist = facehist_form.save(commit=False)
#             facehist.face = face_id
#             facehist.message = message
#             return redirect(self.get_absolute_url())
#         # print('retuest : ',request.POST)
#         # facehist = FaceHist(request.POST)
        
#         # facehist = form.save(commit=False)
#         # facehist.message = message
#         # facehist.face = face_id
#         # facehist.save()
#         # print('facehist : ',facehist)
#         # FaceHist.
#         # return redirect()
#     else:
#         return render(request, 'face/face.html')

class FaceCV(CreateView):
    model=FaceHist
    fields=['age', 'gender', 'image']
    success_url = reverse_lazy(model.get_absolute_url) 
    template_name_suffix = '_create'
    # model.message = '정상처리'


class FaceDV(DetailView):
    model = FaceHist
