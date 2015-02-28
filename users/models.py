from django.db import models

import json
import hashlib
from datetime import datetime
from decimal import Decimal

def exact(str):
    return r'\b' + str + r'\b'


class User(models.Model):
    name 	 = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    age      = models.IntegerField(default=21)

    def __str__(self):
        return self.name + " (" + str(self.age) + ")"

    def dict(self):
        return {'id': str(self.id), 'name': str(self.name), 'password': str(self.password), 'age': self.age}

    def json(self):
        return json.dumps(self.dict())


def UserById(userId):
    result = User.objects.get(id=Decimal(userId))
    return result[0]

def UserByName(name):
    result = User.objects.filter(name__iregex=exact(name))
    return result[0] if len(result) > 0 else None



class UserSong(models.Model):
    user = models.ForeignKey(User)
    songid = models.IntegerField(default=-1)
    rating = models.IntegerField(default=0)

    def dict(self):
        return {'userid': str(self.user.id), 'songid': str(self.songid), 'rating': self.rating}

    def json(self):
        return json.dumps(self.dict())

def FindUserSong(u, songid):
    result = UserSong.objects.filter(user=u).filter(songid=songid)
    return result[0] if len(result) > 0 else None