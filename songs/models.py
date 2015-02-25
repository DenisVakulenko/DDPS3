from django.db import models
import json

class Song(models.Model):
    author = models.CharField(max_length=200)
    name   = models.CharField(max_length=200)

    def __str__(self):
        return self.author + " - " + self.name

    def dict(self):
        return {'id': str(self.id), 'author': str(self.author), 'name': str(self.name)}

    def json(self):
        return json.dumps(self.dict())