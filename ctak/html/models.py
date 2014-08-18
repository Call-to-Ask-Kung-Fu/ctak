from django.contrib.auth.models import User
from django.db import models
import shutil
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from ctak.settings import MEDIA_ROOT

HTML_PATH = 'html/html'
STATIC_PATH = 'html/static'

class Project(models.Model):
    owner = models.ForeignKey(User)
    projectname = models.CharField(max_length=50)
    template_file = models.FileField(upload_to=HTML_PATH)
    static_zip = models.FileField(upload_to=STATIC_PATH, null=True)
    static_url = models.URLField()

    def __unicode__(self):
        return self.projectname

@receiver(pre_delete, sender=Project)
def all_delete(sender, instance, **kwargs):

    instance.template_file.delete(False)
    instance.static_zip.delete(False)
    instance.static_url = 'html/static/%s' % (instance.projectname)
    shutil.rmtree('%s/%s' % (MEDIA_ROOT, instance.static_url))
