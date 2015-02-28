from django.db import models

import json
import hashlib
from datetime import datetime
from decimal import Decimal


def exact(str):
    return r'\b' + str + r'\b'


class Cookie(models.Model):
    userId = models.DecimalField(max_digits=10, decimal_places=0)
    token = models.CharField(max_length=64)

    def dict(self):
        return {'id': str(self.id), 'name': str(self.name), 'password': str(self.password), 'age': self.age}

    def json(self):
        return json.dumps(self.dict())


def generateCookie(userId):
    cookie = Cookie()
    cookie.userId = userId
    cookie.token = hashlib.md5(userId + str(datetime.now().microsecond)).hexdigest()
    while len(Cookie.objects.filter(token__iregex=exact(cookie.token))) > 0:
        cookie.token = hashlib.md5(userId + str(datetime.now().microsecond)).hexdigest()
    cookie.save()
    return cookie


def getCookie(token):
    result = Cookie.objects.filter(token__iregex=exact(token))
    return result[0] if len(result) > 0 else None

def deleteCookie(token):
    result = Cookie.objects.filter(token__iregex=exact(token))
    result[0].delete() if len(result) > 0 else None