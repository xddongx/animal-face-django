from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import FormView
from .models import Face, FaceHist, FaceScore
from .forms import FaceForm
from django.urls import reverse_lazy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
import smtplib, os, re, sys, pdfkit, datetime, time
from datetime import date
from config import keys
from django.conf import settings
from xhtml2pdf import pisa 
from face import face
from werkzeug.utils import secure_filename



# 분석 시작 
def FaceCV(request):
    message = '정상처리'                                    # 정상처리 메세지
    face_kinds = ['고양이상', '공룡상', '토끼상']

    if request.method == 'POST':
        form = request.POST
        facehist_form = FaceHist()                          # 정장될 테이블 명
        facehist_form.age = form['age_field']               # 나이 필드
        facehist_form.gender = form['gender_field']         # 성별 필드
        facehist_form.image = request.FILES['image_field']  # 이미지 필드
        
        facehist_form.message = message                     # 처리되는 상태 메세지
        facehist_form.save()                                # 사용자 기록 저장

        fileName = request.FILES['image_field'].name        # 이미지 파일 이름
        
        face_id, scores = face.animalmodel(fileName)        # 이미지 분석 결과, 점수들
        facehist_form.face = Face.objects.get(kind=face_id) # 분석 얼굴상 결과
        
        facehist_form.kinds = face_kinds                    # 얼굴상의 종류
        facehist_form.scores = scores                       # 얼굴상의 점수들
        facehist_form.save()

        return redirect(facehist_form.get_absolute_url())  # 분석 후 결과 페이지 
    else:
        return render(request, 'face/face.html')


# 분석 결과 페이지
class FaceDV(DetailView):
    model = FaceHist                                        # 불러올 데이터

# 결과 과를 받을 방법
def FaceModal(request):
    if request.method == 'POST':
        form = request.POST
        result_pk = form['pk']                              # form으로 받은 pk
        if form['location'] == 'e-mail':                    # e-mail로 받기
            send_mail(result_pk, form['id'])                # e-mail보내는 함수 호출
            
            print('sent - email')                
            return redirect('animal:index')                 # 전송 성공시 메인화면으로
        return redirect('face:create')


# pdf파일을 생성하기 위한 잠깐의 화면 화면에 보여지지 않음
def Screenshot(request, pk):
    facehist = FaceHist.objects.get(pk=pk)
    context ={
        'facehist': facehist,
    }
    return render(request, 'face/screenshot.html', context)

# pdf파일 제작
def generate_PDF(result_pk):
    url = 'http://localhost:8000/face/facehist/{}/screenshot'.format(result_pk)         # pdf 제작시 화면 url 보여지지는 않는다.
    time.sleep(3)
    filename = time.strftime('%d-%H-%M')                                                # 저장될 pdf이름 일-시간-분

    toyear = str(time.strftime('%Y'))                                                   # 현제 년도
    tomonth = str(time.strftime('%m'))                                                  # 현제 월
    dir_path = './_media/media/pdf/'                                                    # 제작된 pdf저장 경로

    if not(os.path.isdir(dir_path+toyear)):                                             # 년도 폴더유무 확인 후 없으면 제작
        os.mkdir(os.path.join(dir_path+toyear))                                             
        if not(os.path.isdir(dir_path+toyear+tomonth)):                                 # 월 폴더 유무 확인 후 없으면 제작
            os.mkdir(os.path.join(dir_path+toyear+'/'+tomonth))


    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')       # pdf 파일 제작을 도와주는 페키지
    pdfkit.from_url(url, './_media/media/pdf/{}/{}/{}.pdf'.format(toyear,tomonth, filename), configuration=config)     # 저장될 경로 파일이름

    # return redirect('animal:index')


# e-mail 보내기
def send_mail(pk, cl_id):

    data = MIMEMultipart()
    data['Subject'] = '동물상'                          # e-mail 제목
    data['From'] = keys.G_MAILE_ID                     # e-mail 보내는 아이디
    data['To'] = cl_id                                 # 받을 사람 아이디

    # 텍스트 형식의 본문 내용
    text = '요청하신 파일로 전송되었습니다.'             # 전송 문구
    msg = MIMEText(text, 'plain')
    data.attach(msg)

    # pdf 형식의 본문 내용
    generate_PDF(pk)                                    # pdf 파일 제작
    toyear = str(time.strftime('%Y'))                   
    tomonth = str(time.strftime('%m'))
    filename = time.strftime('%d-%H-%M')
    file_path = './_media/media/pdf/'+toyear+'/'+tomonth+'/'+filename+'.pdf'        # 제작된 pdf의 파일 경로

    attach_binary = MIMEBase('application', 'octect-stream')
    pdf = open(file_path,'rb')
    part = MIMEApplication(pdf.read(), name='동물상.pdf')                   # 보낼 pdf파일 이름
    data.attach(part)
    
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
    server.sendmail(keys.G_MAILE_ID, cl_id, data.as_string())
    # quit을 보내고 접속을 종료하고 메일을 보낸다.
    server.quit()

