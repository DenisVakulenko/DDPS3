from django.db import models
import json


class User(models.Model):
    name 	 = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    age      = models.IntegerField(default=21)

    def __str__(self):
        return self.name + " (" + self.age + ")"

    def dict(self):
        return {'id': str(self.id), 'name': str(self.name), 'password': str(self.password), 'age': self.age}

    def json(self):
        return json.dumps(self.dict())


class UserSong(models.Model):
    user = models.ForeignKey(User)
    songid = models.IntegerField(default=-1)
    rating = models.IntegerField(default=0)

    def dict(self):
        return {'user': str(self.user), 'songid': str(self.songid), 'rating': self.rating}

    def json(self):
        return json.dumps(self.dict())