from django.shortcuts import render
from django.http import HttpResponse

# from songs.models import Song
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponse, HttpResponseRedirect
from django import forms

from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import urllib, urllib2

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def index(request):
    s = {}
    checkcookie(request, s)
    return render(request, 'main.html', s)


def checkcookie(request, dict):
    if request.COOKIES.has_key('sessiontoken'):
        t = request.COOKIES['sessiontoken']
        s = requests.get('http://127.0.0.1:8000/mysessions/' + t + '/')
        s = json.loads(s.content)
        if s['valid'] == 'yes':
            u = requests.get('http://127.0.0.1:8000/users/' + s['id'])
            u = json.loads(u.content)
            dict['username'] = u['name']
            dict['userid'] = u['id']


class LoginForm(forms.Form):
    name     = forms.CharField(label='Name', max_length=200)
    password = forms.CharField(label='Pass', max_length=200)
def login(request):
    if request.method == 'POST':
        u = requests.get('http://127.0.0.1:8000/users/check/?name=' + request.POST['name'] + '&password=' + request.POST['password'])
        u = json.loads(u.content)
        if u['id'] != '-1':
            r = HttpResponse(index(request))
            s = requests.put('http://127.0.0.1:8000/mysessions/?userid=' + u['id'])
            s = json.loads(s.content)
            set_cookie(r, 'sessiontoken', s['token'])
            return r

        form = LoginForm()
        return render(request, 'form.html', {'form':form, 'msg':"wrong user or pass"})
    form = LoginForm()
    return render(request, 'form.html', {'form':form})

def logout(request):
    if request.COOKIES.has_key('sessiontoken'):
        t = request.COOKIES['sessiontoken']
        s = requests.delete('http://127.0.0.1:8000/mysessions/' + t + '/')
    r = HttpResponse(index(request))
    r.delete_cookie('sessiontoken')
    return r


import datetime

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)


def users(request):
    page = request.GET.get('page') if ('page' in request.GET) else '1'
    s = requests.get('http://127.0.0.1:8000/users/?page=' + page)
    s = json.loads(s.content)
    s["url"] = "http://127.0.0.1:8000/front/users/"
    checkcookie(request, s)
    return render(request, 'userslist.html', s)

def user(request):
    s = requests.get('http://127.0.0.1:8000/users/' + request.path.split('/')[3] + '/songs/')
    s = json.loads(s.content)
    print s

    l = []
    for i in s:
        ss = requests.get('http://127.0.0.1:8000/songs/' + i['songid'] + '/')
        if ss.status_code == 200:
            ss = json.loads(ss.content)
            print ss

            us = requests.get('http://127.0.0.1:8000/users/' + i['userid'] + '/songs/' + i['songid'] + '/')
            us = json.loads(us.content)
            if us['rating'] != '-1':
                ss['rating'] = us['rating']

            l.append(ss)

    c = {'content': l}
    checkcookie(request, c)
    return render(request, 'songslist.html', c)

class EditUserForm(forms.Form):
    name     = forms.CharField(label='Name', max_length=200)
    password = forms.CharField(label='Pass', max_length=200)
    age      = forms.CharField(label='Age', max_length=200)
    id       = forms.CharField(initial=-1, widget=forms.widgets.HiddenInput())
def edituser(request):
    if request.method == 'POST':
        if request.POST['id'] == '-1':
            requests.put('http://127.0.0.1:8000/users/?name=' + request.POST['name'] + '&password=' + request.POST['password'] + '&age=' + request.POST['age'])
        else:
            data = {'name': request.POST['name'], 'password': request.POST['password'], 'age': request.POST['age']}
            requests.post('http://127.0.0.1:8000/users/' + request.POST['id'] + '/', data)
        return HttpResponseRedirect("http://127.0.0.1:8000/front/users/?page=100500")
    else:
        form = EditUserForm()
        if 'id' in request.REQUEST and request.REQUEST['id'] != -1:
            s = requests.get('http://127.0.0.1:8000/users/' + request.REQUEST['id'])
            s = json.loads(s.content)
            form = EditUserForm({'name': s['name'], 'password': s['password'], 'age': s['age'], 'id': s['id']})
    f = {'form': form}
    checkcookie(request, f)
    return render(request, 'form.html', f)


def backusers(request):
    # if request.method == 'GET':
    #     page = request.GET.get('page') if ('page' in request.GET) else '1'
    #     return requests.get('http://127.0.0.1:8000/songs/?page=' + page)
    if request.method == 'PUT':
        return requests.put('http://127.0.0.1:8000/users/?name=' + request.REQUEST['name'] + '&password=' + request.REQUEST['password'] + '&age=' + request.REQUEST['age'])
def backuser(request):
    id = request.path.split('/')[2]
    # if request.method == 'POST':
    #     data = {'name': request.POST['name'], 'author': request.POST['author']}
    #     return requests.post('http://127.0.0.1:8000/songs/' + id + '/', data)
    # if request.method == 'GET':
    #     return requests.get('http://127.0.0.1:8000/songs/' + id + '/')
    if request.method == 'DELETE':
        return requests.delete('http://127.0.0.1:8000/users/' + id + '/')


def songs(request):
    page = request.GET['page'] if ('page' in request.GET) else '1'
    s = requests.get('http://127.0.0.1:8000/songs/?page=' + page)
    s = json.loads(s.content)
    checkcookie(request, s)
    if 'userid' in s:
        arr = []
        for i in s['content']:
            arr.append(i['id'])

        p = {'ids[]': arr}
        us = requests.get('http://127.0.0.1:8000/users/' + s['userid'] + '/songs/byids/', params=p)
        us = json.loads(us.content)

        for i in us:
            sid = i['songid']
            for j in s['content']:
                if j['id'] == sid:
                    j['rating'] = i['rating']

    s["url"] = "http://127.0.0.1:8000/front/songs/"
    return render(request, 'songslist.html', s)

def song(request):




    s = requests.get('http://127.0.0.1:8000/songs/' + request.REQUEST['id'])
    s = json.loads(s.content)
    c = {'songs_list': s.content}
    checkcookie(request, c)
    return render(request, 'songslist.html', c)

class EditSongForm(forms.Form):
    name     = forms.CharField(label='Name', max_length=200)
    author   = forms.CharField(label='Author', max_length=200)
    id       = forms.CharField(initial=-1, widget=forms.widgets.HiddenInput())
def editsong(request):
    if request.method == 'POST':
        if request.POST['id'] == '-1':
            requests.put('http://127.0.0.1:8000/songs/?name=' + request.POST['name'] + '&author=' + request.POST['author'])
        else:
            data = {'name': request.POST['name'], 'author': request.POST['author']}
            requests.post('http://127.0.0.1:8000/songs/' + request.POST['id'] + '/', data)
        return HttpResponseRedirect("http://127.0.0.1:8000/front/songs/?page=100500")
    else:
        form = EditSongForm()
        if 'id' in request.REQUEST and request.REQUEST['id'] != -1:
            s = requests.get('http://127.0.0.1:8000/songs/' + request.REQUEST['id'])
            s = json.loads(s.content)
            form = EditSongForm({'name': s['name'], 'author': s['author'], 'id': s['id']})
    f = {'form': form}
    checkcookie(request, f)
    return render(request, 'form.html', f)


def backsongs(request):
    if request.method == 'GET':
        page = request.GET['page'] if ('page' in request.GET) else '1'
        return HttpResponse(requests.get('http://127.0.0.1:8000/songs/?page=' + page))
    if request.method == 'PUT':
        return HttpResponse(requests.put('http://127.0.0.1:8000/songs/?name=' + request.REQUEST['name'] + '&author=' + request.REQUEST['author']))
@csrf_exempt
def backsong(request):
    id = request.path.split('/')[3]
    if request.method == 'POST':
        data = {'name': request.POST['name'], 'author': request.POST['author']}
        return HttpResponse(requests.post('http://127.0.0.1:8000/songs/' + id + '/', data))
    if request.method == 'GET':
        return HttpResponse(requests.get('http://127.0.0.1:8000/songs/' + id + '/'))
    if request.method == 'DELETE':
        return HttpResponse(requests.delete('http://127.0.0.1:8000/songs/' + id + '/'))

@csrf_exempt
def ratesong(request):
    return HttpResponse(requests.put('http://127.0.0.1:8000/users/' + request.REQUEST['uid'] + '/songs/' + request.REQUEST['sid'] + '/?rating=' + request.REQUEST['r']))
@csrf_exempt
def unratesong(request):

    return HttpResponse(requests.delete('http://127.0.0.1:8000/users/' + request.REQUEST['uid'] + '/songs/' + request.REQUEST['sid'] + '/'))


def debug(msg):
    print "DEBUG: " + str(msg)