from django.shortcuts import render
from xvideo.models import detail
from django.core.paginator import Paginator
import random

type_dic = {
        "1":['自拍视频 ','国产自拍','亚洲视频 '],
        "2":["日韩无码",'无码视频 '],
        "3":["日韩有码",'有码视频 '],
        "4":["欧美极品",'欧美视频 '],
        "5":["动漫精品",'动漫视频 '],
        "6":["中文字幕 ",'中文字幕'],
        "7":["一本道 ","东京热 "],
        "8":["极骚萝莉",'童颜巨乳','绝美少女'],
        "9":["重咸口味",'人妖视频','强奸乱伦'],
        "10":["JAVHD ",'伦理片 ','高潮喷吹','独家DMM','HEY诱惑','HEYZO','激情口交','VR视频 ','首次亮相'
              ,'女女视频 ','群交视频 ','辣椒GIGA','三级自慰','独家擂台格斗']
    }
# Create your views here.
def index(request):
    news = detail.objects.filter().order_by('-updateTime')[0:6]
    domselfs = detail.objects.filter(type__in=type_dic.get('1')).order_by("-updateTime")[0:12]
    jknocodes = detail.objects.filter(type__in=type_dic.get('2')).order_by("-updateTime")[0:12]
    jknodes = detail.objects.filter(type__in=type_dic.get('3')).order_by("-updateTime")[0:12]
    europeames = detail.objects.filter(type__in=type_dic.get('4')).order_by("-updateTime")[0:12]
    dongman = detail.objects.filter(type__in=type_dic.get('5')).order_by("-updateTime")[0:12]
    context = {}
    context["news"] = news
    context["domselfs"] = domselfs
    context['jknocodes'] = jknocodes
    context['jknodes'] = jknodes
    context['europeames'] = europeames
    context['dongman'] = dongman
    return render(request, 'xvideo/index.html', context)

def play(request):
    id = request.GET.get("id")
    videos = detail.objects.get(id=id)
    relate_movie = detail.objects.filter(type=videos.type).values("id","name","image")
    relate_movies = relate_movie[0:min(200,relate_movie.count())]
    r_m = []
    if relate_movies:
        r_m = random.sample(list(relate_movies), 12)
    return render(request, 'xvideo/play.html',{"videos":videos, "r_m":r_m})

def more(request):
    t = request.GET.get('t')
    movies = detail.objects.filter(type__in=type_dic.get(t)).order_by('-updateTime')
    page = request.GET.get('page',1)
    paginator = Paginator(movies, 30)
    page = paginator.page(page)
    return render(request, 'xvideo/more.html', {'page': page, 't': t })

def search(request):
    key = ""
    page = 1
    if request.POST:
        key = request.POST.get('searchword',default='你好')
    else:
        key = request.GET.get("k")
        page = request.GET.get('page')
    movies = detail.objects.filter(name__contains=key)
    paginator = Paginator(movies, min(30,movies.count()))
    page = paginator.page(page)
    return render(request, 'xvideo/search.html',{'page': page,'key':key})
