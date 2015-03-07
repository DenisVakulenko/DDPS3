from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import urllib, urllib2

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import csrf_exempt


from models import User, UserByName, UserSong, FindUserSong




@csrf_exempt
def usersongs_byids(request):
    if request.method == 'GET':
        id = request.path.split('/')[2]
        u = User.objects.get(id=id)

        ans = []
        songids = request.GET.getlist('ids[]')
        for songid in songids:
            s = FindUserSong(u, songid)
            if s:
                ans.append(s.dict())

        if ans:
            print 'arr req --'
            print ans
            print 'arr req --'
            return HttpResponse(json.dumps(ans), content_type="application/json")
        return HttpResponse(json.dumps({'rating': '-1'}), content_type="application/json")


@csrf_exempt
def usersongs(request):
    if request.method == 'GET':
        id = request.path.split('/')[2]
        u = User.objects.get(id=id)
        s = UserSong.objects.filter(user=u)
        s = [rec.dict() for rec in s]
        return HttpResponse(json.dumps(s), content_type="application/json")

@csrf_exempt
def usersong(request):
    if request.method == 'GET':
        id = request.path.split('/')[2]
        songid = request.path.split('/')[4]
        u = User.objects.get(id=id)
        s = FindUserSong(u, songid)
        if s:
            return HttpResponse(s.json(), content_type="application/json")
        return HttpResponse(json.dumps({'rating': '-1'}), content_type="application/json")

    if request.method == 'PUT':
        id = request.path.split('/')[2]
        songid = request.path.split('/')[4]
        u = User.objects.get(id=id)
        us = UserSong(user=u, songid=songid, rating=request.REQUEST['rating'])
        us.save()
        return HttpResponse(us.json(), content_type="application/json")

    if request.method == 'DELETE':
        id = request.path.split('/')[2]
        songid = request.path.split('/')[4]
        u = User.objects.get(id=id)
        s = UserSong.objects.filter(user=u).filter(songid=songid)
        s.delete()
        return HttpResponse("{ 'ok' : 'ok' }", content_type="application/json")


def checksong(request):
    if request.method == 'GET':
        name=request.REQUEST['name']
        password=request.REQUEST['password']

        u = UserByName(name)

        if u:
            if u.password == password:
                return HttpResponse(u.json(), content_type="application/json")



@csrf_exempt
def user(request):
    if request.method == 'POST':
        id = request.path.split('/')[2]
        s = User.objects.get(id=id)
        s.name=request.REQUEST['name']
        s.password=request.REQUEST['password']
        s.age=request.REQUEST['age']
        s.save()
        return HttpResponse(s.json(), content_type="application/json")
    if request.method == 'GET':
        id = request.path.split('/')[2]
        s = User.objects.get(id=id)
        return HttpResponse(s.json(), content_type="application/json")
    if request.method == 'DELETE':
        id = request.path.split('/')[2]
        s = User.objects.get(id=id)
        s.delete()
        return HttpResponse("{ 'ok' : 'ok' }", content_type="application/json")


# def user(request):
#     if request.method == 'GET':
#         id = request.path.split('/')[2]
#         s = User.objects.get(name=id)
#         return HttpResponse(s.json(), content_type="application/json")


def check(request):
    if request.method == 'GET':
        name=request.REQUEST['name']
        password=request.REQUEST['password']

        u = UserByName(name)

        if u:
            if u.password == password:
                return HttpResponse(u.json(), content_type="application/json")

        return HttpResponse(json.dumps({'id': '-1'}), content_type="application/json")


@csrf_exempt
def users(request):
    if request.method == 'PUT':
        s = User(name=request.REQUEST['name'], password=request.REQUEST['password'], age=request.REQUEST['age'])
        s.save()
        return HttpResponse(s.json(), content_type="application/json")
    if request.method == 'GET':
        records = User.objects.all()
        p = Paginator([rec.dict() for rec in records], 5)

        if 'page' in request.GET:
            page = request.GET.get('page')
        else:
            page = 1

        try:
            records_json = p.page(page).object_list
        except PageNotAnInteger:
            page = 1
            records_json = p.page(page).object_list
        except EmptyPage:
            page = p.num_pages
            records_json = p.page(page).object_list

        c = json.dumps(records_json)
        return HttpResponse('{ "page" : ' + str(page) + ', "pages" : ' + str(p.num_pages) + ', "content" : ' + c + '}', content_type="application/json")


# Song(name='Kashmir', author='Led Zeppelin').save()
# Song(name='Immigrant Song', author='Led Zeppelin').save()
# Song(name='The End', author='Doors').save()
# Song(name='God Gave Rock\'N\'Roll To You', author='Kiss').save()
