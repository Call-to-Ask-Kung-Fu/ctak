from __future__ import division
import os
from django.db import models
from django.contrib.auth.models import User
import datetime
from PIL import Image, ImageOps
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
now = datetime.datetime.now()
date = (now.year, now.month, now.day)
AIMAGE_PATH = 'producer/img/avatar/%s/%s/%s' % date
ATHUMB_PATH = 'producer/img/avatar/%s/%s/%s/thumb' % date


class Producer(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    sexes = (('Male', 'Male'), ('Female', "Female"), ('Other', 'Other'),)
    sex = models.CharField(max_length=20, choices=sexes, default='Other', blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.nickname

class Avatar(models.Model):
    owner = models.ForeignKey(Producer)
    upload_time = models.DateTimeField()
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=AIMAGE_PATH, height_field=None, width_field=None, max_length=100, null=True)
    thumb1 = models.ImageField(upload_to=ATHUMB_PATH, blank=True)
    thumb2 = models.ImageField(upload_to=ATHUMB_PATH, blank=True)

    def save(self):
        def create_thumbnail(self):
            if not self.image:
                return
            DJANGO_TYPE = self.image.file.content_type
            if DJANGO_TYPE == 'image/jpeg':
                PIL_TYPE = 'jpeg'
                FILE_EXTENSION = 'jpg'
            elif DJANGO_TYPE == 'image/png':
                PIL_TYPE = 'png'
                FILE_EXTENSION = 'png'
            image = Image.open(StringIO(self.image.read()))
            w, h = image.size
            if w > 640:
                delta = w / 640
                h = int(h / delta)
                THUMBNAIL_SIZE2 = (640, h)
                thumb = ImageOps.fit(image, THUMBNAIL_SIZE2, Image.ANTIALIAS)
                temp_handle = StringIO()
                thumb.save(temp_handle, PIL_TYPE)
                temp_handle.seek(0)
                suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
                self.image.save('%s_thumbnail1.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)
            size = 300
            THUMBNAIL_SIZE1 = (size, size)
            thumb1 = ImageOps.fit(image, THUMBNAIL_SIZE1, Image.ANTIALIAS)
            temp_handle = StringIO()
            thumb1.save(temp_handle, PIL_TYPE)
            temp_handle.seek(0)
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
            self.thumb1.save('%s_thumbnail1.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)
            width, height = image.size
            delta = width / size
            height = int(height / delta)
            THUMBNAIL_SIZE2 = (size, height)
            thumb2 = ImageOps.fit(image, THUMBNAIL_SIZE2, Image.ANTIALIAS)
            temp_handle = StringIO()
            thumb2.save(temp_handle, PIL_TYPE)
            temp_handle.seek(0)
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
            self.thumb2.save('%s_thumbnail1.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)
        create_thumbnail(self)

        super(Avatar, self).save()

    def __unicode__(self):
        return self.name

@receiver(pre_delete, sender=Avatar)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.thumb1.delete(False)
    instance.thumb2.delete(False)
