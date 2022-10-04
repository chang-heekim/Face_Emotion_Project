from django.shortcuts import render, redirect
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse
import cv2
import threading
from cnn_emotion.work import predict_emotion
from cnn_emotion.model import VGG
from cnn_emotion.web_crawling import find_music
import time
import torch
from torchvision.models import vgg19_bn
# Create your views here.


def main(request):
    return render(request, 'main.html')


def bad_request(request, exception):
    return render(request, '400.html', status=400)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.ret, self.frame = self.video.read()
        threading.Thread(target=self.update, args=()).start()

        self.path = 'cnn_emotion/best_model.pth'
        self.model = 'cnn_emotion/res10_300x300_ssd_iter_140000_fp16.caffemodel'
        self.config = 'cnn_emotion/deploy.prototxt.txt'

        self.emotion_model, self.net = self.init_model(
            self.path, self.model, self.config)

        _, self.emotion = predict_emotion(
            self.frame, self.net, self.emotion_model)

    def turn_off(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image, _ = predict_emotion(
            image, self.net, self.emotion_model)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            self.ret, self.frame = self.video.read()

    def init_model(self, dnn_path, detect_model_path, detect_config_path):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        base_model = vgg19_bn(weights=None).features
        emotion_model = VGG(base_model, n_classes=7)
        emotion_model.load_state_dict(
            torch.load(dnn_path, map_location=device))
        emotion_model.eval()
        net = cv2.dnn.readNet(detect_model_path, detect_config_path)
        return emotion_model, net


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def emotion_detector(request, isTrue):
    try:
        cam = VideoCamera()
        if isTrue == 'on':
            return StreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace;boundary=frame')
        elif isTrue == 'off':
            cam.turn_off()
            return HttpResponse()

    except:
        print("에러입니다...")
        pass


def recomendation(request, isTrue):
    if isTrue == 'on':
        cam = VideoCamera()
        emotion = cam.emotion
        if emotion == 'neutral':
            return render(request, 'main.html', {'msg': 'Make a face'})
        else:
            titles, singers = find_music(emotion)
            data = zip(titles, singers)
            context = {'data': data, 'emotion': emotion}
            return render(request, 'main.html', context)
    elif isTrue == 'off':
        return render(request, 'main.html', {'msg': 'Turn On Camera'})
