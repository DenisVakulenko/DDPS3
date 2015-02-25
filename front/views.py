from django.shortcuts import render
from django.http import HttpResponse

# from songs.models import Song
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import urllib, urllib2

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    return HttpResponse('hi')


def songs(request):
    page = request.GET.get('page') if ('page' in request.GET) else '1'

    s = requests.get('http://127.0.0.1:8000/songs/?page=' + page)
    s = json.loads(s.content)
    s["url"] = "http://127.0.0.1:8000/front/songs/"
    return render(request, 'songslist.html', s)

def song(request):
    s = requests.get('songs/')
    json.loads(s)
    c = {'songs_list': s.content}
    return render(request, 'songslist.html', c)


def debug(msg):
    print "DEBUG: " + str(msg)