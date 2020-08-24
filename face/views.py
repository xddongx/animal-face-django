from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormView
from .models import Face, FaceHist
from .forms import FaceForm
from django.urls import reverse_lazy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import smtplib, os, re, sys, pdfkit, datetime, time
from datetime import date
from config import keys
from django.conf import settings
from xhtml2pdf import pisa 
from django.template import Context
from django.template.loader import get_template
from io import StringIO


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
        context = {}
        context['face'] = face_id


        return redirect(facehist_form.get_absolute_url(), context)
    else:
        return render(request, 'face/face.html')


class FaceDV(DetailView):
    model = FaceHist

def FaceModal(request):
    if request.method == 'POST':
        form = request.POST
        if form['location'] == 'e-mail':
            face_pk = FaceHist.objects.get(pk=form['pk'])
            data = MIMEMultipart('SendMail')
            data['Subject'] = '동물상'
            data['From'] = keys.G_MAILE_ID
            data['To'] = form['id']
            # 텍스트 형식의 본문 내용
            text = '선택하신 파일로 전송되었습니다.'
            msg = MIMEText(text, 'plain')
            data.attach(msg)
            print(data)

            # 이미지 전송 실패
            # 텍스트 전송 선공


            # 메일 서버와 telnet 통신 개시
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # 메일 통신시 디버그
            server.set_debuglevel(1)
            # 헤로 한번 해주자(의미없음)
            server.ehlo()
            # tls 설정 주문 -tls 587 포트의 경우
            # server.starttls
            server.login(keys.G_MAILE_ID, keys.G_MAILE_PASSWORD)
            # 메일 프로토콜 상 mail, rcpt, data순으로 메시지를 보내야 하는데 이걸 sendmail 함수에서 자동으로 해준다.
            server.sendmail(keys.G_MAILE_ID, form['id'], data.as_string())
            # quit을 보내고 접속을 종료하고 메일을 보낸다.
            server.quit()

            print('sent')                
            return redirect('face:create')
        return redirect('face:create')

def Screenshot(request, pk):

    facehist = FaceHist.objects.get(pk=pk)
    face_id = Face.objects.get(pk=facehist.face.pk)
    context ={
        'image': facehist.image,
        'face': face_id,
    }
    return render(request, 'face/screenshot.html', context)


def generate_PDF(request):
    pk_ = 17

    url = 'http://localhost:8000/face/facehist/{}/screenshot'.format(pk_)
    filename = time.strftime('%d-%H-%M')

    toyear = str(time.strftime('%Y'))
    tomonth = str(time.strftime('%m'))
    dir_path = './_media/media/pdf/'

    if not(os.path.isdir(dir_path+toyear)):
        os.mkdir(os.path.join(dir_path+toyear))
        if not(os.path.isdir(dir_path+toyear+tomonth)):
            os.mkdir(os.path.join(dir_path+toyear+'/'+tomonth))


    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdfkit.from_url(url, './_media/media/pdf/{}/{}/{}.pdf'.format(toyear,tomonth, filename), configuration=config)

    return redirect('animal:index')

