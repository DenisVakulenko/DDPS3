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
    return render(request, 'main.html')


def users(request):
    page = request.GET.get('page') if ('page' in request.GET) else '1'
    s = requests.get('http://127.0.0.1:8000/users/?page=' + page)
    s = json.loads(s.content)
    s["url"] = "http://127.0.0.1:8000/front/users/"
    return render(request, 'userslist.html', s)

def user(request):
    s = requests.get('http://127.0.0.1:8000/users/' + request.REQUEST['id'])
    s = json.loads(s.content)
    c = {'songs_list': s.content}
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
    return render(request, 'editsong.html', {'form': form})

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
    s["url"] = "http://127.0.0.1:8000/front/songs/"
    return render(request, 'songslist.html', s)

def song(request):
    s = requests.get('http://127.0.0.1:8000/songs/' + request.REQUEST['id'])
    s = json.loads(s.content)
    c = {'songs_list': s.content}
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
    return render(request, 'editsong.html', {'form': form})


def backsongs(request):
    if request.method == 'GET':
        page = request.GET['page'] if ('page' in request.GET) else '1'
        return HttpResponse(requests.get('http://127.0.0.1:8000/songs/?page=' + page))
    if request.method == 'PUT':
        return HttpResponse(requests.put('http://127.0.0.1:8000/songs/?name=' + request.REQUEST['name'] + '&author=' + request.REQUEST['author']))
@csrf_exempt
def backsong(request):
    id = request.path.split('/')[2]
    if request.method == 'POST':
        data = {'name': request.POST['name'], 'author': request.POST['author']}
        return HttpResponse(requests.post('http://127.0.0.1:8000/songs/' + id + '/', data))
    if request.method == 'GET':
        return HttpResponse(requests.get('http://127.0.0.1:8000/songs/' + id + '/'))
    if request.method == 'DELETE':
        return HttpResponse(requests.delete('http://127.0.0.1:8000/songs/' + id + '/'))



def debug(msg):
    print "DEBUG: " + str(msg)