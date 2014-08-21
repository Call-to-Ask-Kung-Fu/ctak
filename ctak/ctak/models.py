from account.models import Producer
from django.db import models

class Index(models.Model):
    project = models.CharField(max_length=50)
    owner = models.ForeignKey(Producer)
    url = models.CharField(max_length=100)
    types = (('Django', 'Django'), ('html', 'html'),)
    type = models.CharField(max_length=20, choices=types)

    def __unicode__(self):
        return self.name
