from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    path = '/data/vip_video/video/result.txt'
    list = []
    with open(path, 'r', encoding="utf-8")as f:
        for url in f.readlines():
            data = {}
            data["name"] = url.split(',')[0]
            data["value"] = url.split(',')[1].strip()
            list.append(data)
    return render(request,'hello.html',{"list":list})

def video(request):
    return render(request,'video.html')

def zhibo(request):
    url = request.GET.get("url")
    response = render(request,'zhibo.html',{"url":url})
    response['Access-Control-Allow-Origin'] = "*"
    return response
