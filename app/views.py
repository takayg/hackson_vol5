from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import StreamingHttpResponse
from django.urls import reverse_lazy

from .models import Activity

from face_detection_management.settings import FACE_CASCADE_PATH

import datetime

import sys
import cv2

import os

class IndexView(generic.TemplateView):

    template_name = 'index.html'

def working(request):
    global start_time
    start_time = datetime.datetime.now()
    context = {
        'start_time' : start_time,
    }
    return render(request, 'working.html', context)


# @login_required
def capture():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if cap.isOpened() is False:
        print("can not open camera")
        sys.exit()

    cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    
    while True:

        # VideoCaptureから1フレーム読み込む
        ret, frame = cap.read()

        # そのままの大きさだと処理速度がきついのでリサイズ
        frame = cv2.resize(frame, (int(frame.shape[1]*0.7), int(frame.shape[0]*0.7)))

        # 処理速度を高めるために画像をグレースケールに変換したものを用意
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 顔検出
        facerect = cascade.detectMultiScale(
            gray,
            scaleFactor=1.11,
            minNeighbors=3,
            minSize=(100, 100)
        )

        if len(facerect) != 0:
            for x, y, w, h in facerect:
                # 顔の部分(この顔の部分に対して目の検出をかける)
                face_gray = gray[y: y + h, x: x + w]

                # 顔検出した部分に枠を描画
                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (255, 255, 255),
                    thickness=2
                )
        
        # フレーム画像をバイナリに変換
        ret, jpeg = cv2.imencode('.jpg', frame)
        byte_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_frame + b'\r\n\r\n')

    # キャプチャをリリースして、ウィンドウをすべて閉じる
    cap.release()

def send_capture():
    return lambda _: StreamingHttpResponse(capture(), content_type='multipart/x-mixed-replace; boundary=frame')

def finish_task(request):
    global start_time
    finish_time = datetime.datetime.now()
    time_diff = (finish_time - start_time)
    time_diff = time_diff.seconds


    activity = Activity.objects.create(
        user = request.user,
        start_time = start_time,
        finish_time = finish_time,
        study_time = time_diff
        #study_time = str(hours) + '時間' + str(minutes) + '分' + str(seconds) + '秒'
    )

    hours = time_diff // 3600
    time_diff %= 3600
    minutes = time_diff // 60
    seconds = time_diff % 60
    context = {'hours' : hours, 'minutes' : minutes, 'seconds' : seconds}

    

    return render(request, 'finish_task.html', context)

class DataList(generic.ListView):

    template_name = 'data_list.html'
    context_object_name = 'activities'
    
    def get_queryset(self):
        activities = Activity.objects.filter(user=self.request.user).order_by('-start_time')
        return activities