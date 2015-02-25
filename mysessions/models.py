from django.db import models
from users.models import User

class MySessions(models.Model):
    session  = models.CharField(max_length=100)
    user 	 = models.ForeignKey(User)
    # host = models.CharField(max_length=100)
    # ip = models.CharField(max_length=200)

    @classmethod
    def create(cls, foruser):
        s = cls(session=foruser.id*234, user = foruser)
        return s
        # self.expirationDate = datetime.now() + timedelta(minutes=20)