from django.shortcuts import render
from film.models import video_detail
from film.models import video_episode
from django.core.paginator import Paginator
import random

# Create your views here.
def index(request):
    newest = video_detail.objects.filter().order_by("-updateTime")[0:6]
    movies = video_detail.objects.filter(type__endswith='片 ').order_by("-updateTime")[0:12]
    tvs = video_detail.objects.filter(type__endswith="剧 ").order_by("-updateTime")[0:12]
    animations = video_detail.objects.filter(type__contains="动漫").order_by("-updateTime")[0:12]
    arts = video_detail.objects.filter(type__contains="综艺").order_by("-updateTime")[0:12]
    context = {}
    context["newest"] = newest
    context["movies"] = movies
    context['tvs'] = tvs
    context['animations'] = animations
    context['arts'] = arts
    return render(request, 'film/kanju.html',context)

def detail(request):
    nameMd5 = request.GET.get('name',default='0')
    movie = video_detail.objects.get(nameMd5=nameMd5)
    episodes = video_episode.objects.filter(nameMd5=nameMd5).order_by('episodeMd5')
    #同类型的视频
    relate_movies = video_detail.objects.filter(type=movie.type).values("name","nameMd5","image","score","updateTo")[0:100]
    r_m = []
    if relate_movies:
        r_m = random.sample(list(relate_movies), 12)

    context = {}
    context["movie"] = movie
    context['episodes'] = episodes
    context['r_m'] = r_m
    return render(request, 'film/detail.html',context)

def play(request):
    nameMd5 = request.GET.get('name',default='0')
    episodeMd5 = request.GET.get('episode',default='0')
    episode = video_episode.objects.filter(nameMd5=nameMd5, episodeMd5=episodeMd5).first()
    episodes = video_episode.objects.filter(nameMd5=nameMd5).order_by('episodeMd5').values("episode","episodeMd5")
    #计算上一集 下一集
    list_episodes = []
    episodes_len = len(episodes)
    for i in range(0,episodes_len):
        list_episodes.append(episodes[i]["episodeMd5"])
    episode_index = list_episodes.index(int(episodeMd5))
    episode_previous = list_episodes[episode_index-1] if episode_index - 1 >= 0 else ""
    episode_next = list_episodes[episode_index+1] if episode_index + 1 < episodes_len else ""

    return render(request, 'film/play.html', {'episode':episode, 'episodes':episodes, "episode_previous":episode_previous,
                                              "episode_next":episode_next})

def search(request):
    key = ""
    page = 1
    if request.POST:
        key = request.POST.get('searchword',default='你好')
    else:
        key = request.GET.get("k")
        page = request.GET.get('page')
    movies = video_detail.objects.filter(name__contains=key).order_by('-score')
    paginator = Paginator(movies, 10)
    page = paginator.page(page)
    return render(request, 'film/search.html',{'page': page,'key':key})

def more(request):
    type_dict = {'1':'片,1','2':'剧,2','3':'动漫,3','4':'综艺,4'
                ,'5':'动作片,1','6':'喜剧片,1','7':'爱情片,1','8':'科幻片,1','9':'剧情片,1','10':'恐怖片,1','11':'战争片,1','12':'纪录片,1','13':'伦理片,1'
                ,'14':'国产剧,2','15':'香港剧,2','16':'韩国剧,2','17':'欧美剧,2','18':'台湾剧,2','19':'日本剧,2','20':'海外剧,2'
                ,'21':'内地综艺,4','22':'港台综艺,4','23':'日韩综艺,4','24':'欧美综艺,4'
                ,'25':'国产动� ,3','26':'日韩动� ,3','27':'港台动漫,3','28':'欧美动漫,3','29':'海外动漫,3'
                 ,'30':'福利,1'}

    t = request.GET.get('t')
    re = request.GET.get('re',default="")
    ti = request.GET.get('ti',default="")
    dic_data = {}
    if re != "":
        dic_data['region'] = re
    if ti != "":
        dic_data['issueTime'] = ti
    typeValue = type_dict.get(t).split(',')[0]
    t_parent = type_dict.get(t).split(',')[1]
    if int(t) >= 5:
        dic_data['type'] = typeValue
    if t in ['1','2','3','4']:
        movies = video_detail.objects.filter(type__endswith=typeValue,**dic_data).order_by('-updateTime')
    else:
        movies = video_detail.objects.filter(**dic_data).order_by('-updateTime')
    page = request.GET.get('page',1)
    paginator = Paginator(movies, 30)
    page = paginator.page(page)

    return render(request, 'film/more.html', {'page': page, 't': t, 're':re, 'ti':ti, 't_parent':t_parent })

def global_settings(request):
    dic_channel = {"1":"电影","2":"电视剧","4":"综艺","3":"动漫"}

    dic_type_me = {"1":'全部','5':'动作片','6':'喜剧片','7':'爱情片','8':'科幻片','9':'剧情片','10':'恐怖片','11':'战争片',
                   '12':'纪录片','13':'伦理片','30':'福利片'}
    dic_type_tv = {"2":'全部','14':'国产剧','15':'香港剧','16':'韩国剧','17':'欧美剧','18':'台湾剧','19':'日本剧','20':'海外剧'}
    dic_type_art = {"4":'全部','21':'内地综艺','22':'港台综艺','23':'日韩综艺','24':'欧美综艺'}
    dic_type_am = {"3":'全部','25':'国产动漫','26':'日韩动漫','27':'港台动漫','28':'欧美动漫','29':'海外动漫'}

    dic_region = {"":"全部","中国大陆":"中国大陆","香港":"香港","台湾":"台湾","美国":"美国","法国":"法国","英国":"英国","日本":"日本","韩国":"韩国",
                  "德国":"德国","泰国":"泰国","印度":"印度","意大利":"意大利","西班牙":"西班牙","加拿大":"加拿大","其它":"其它"}
    dic_time = {"":"全部","2020":"2020","2019":"2019","2018":"2018","2017":"2017","2016":"2016","2015":"2015","2014":"2014","2013":"2013","2012":"2012","2011":"2011","2010":"2010"}

    return {
        "dic_channel":dic_channel,
        "dic_type_me":dic_type_me,
        "dic_type_tv":dic_type_tv,
        "dic_type_art":dic_type_art,
        "dic_type_am":dic_type_am,
        "dic_region":dic_region,
        "dic_time":dic_time,
    }

def jiexi(request):
    url = request.GET.get('url')
    return render(request, 'film/jiexi.html', {"url":url})
