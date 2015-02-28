from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import json
from mysessions import models
from django.views.decorators.csrf import csrf_exempt


def check(request):
    if request.method == 'GET':
        get = request.GET

        token = get.get('token')
        userId = get.get('userID')

        result = {}
        cookie = models.getCookie(token)
        if cookie:
            result["valid"] = 1
        else:
            result["error"] = 1

        return HttpResponse(json.dumps(result))

@csrf_exempt
def handle(request):
    if request.method == 'GET':
        token = request.path.split('/')[2]
        result = {}
        cookie = models.getCookie(token)
        if cookie:
            result["valid"] = 'yes'
            result["id"] = str(cookie.userId)
        else:
            result["valid"] = 'no'

        return HttpResponse(json.dumps(result))
    if request.method == 'PUT':
        id = request.REQUEST['userid']

        result = {}
        cookie = models.generateCookie(id)
        result['id'] = cookie.userId
        result['token'] = cookie.token
        return HttpResponse(json.dumps(result))
    if request.method == 'DELETE':
        token = request.path.split('/')[2]

        cookie = models.getCookie(token)
        if cookie:
            cookie.delete()

        return HttpResponse(json.dumps({'ok': 'ok'}))


def handleMeRequest(request):
    get = request.GET

    userId = get.get('id')
    user = models.getUserViaId(userId)

    return HttpResponse(user.json())