from django.db import models
import datetime
import qrcode
from PIL import Image, ImageOps
from cStringIO import StringIO
import os

now = datetime.datetime.now()
date = (now.year, now.month, now.day)
ICON_PATH = 'qr/icon/%s/%s/%s' % date
QR_PATH = 'qr/png/%s/%s/%s' % date
from django.core.files.uploadedfile import SimpleUploadedFile

def make_qr(self):
    FILE_EXTENSION = 'png'
    temp_handle = StringIO()

    infile = self.input
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=1
        )
    qr.add_data(infile)
    qr.make(fit=True)
    img = qr.make_image()
    if not self.icon:
        img.save(temp_handle, FILE_EXTENSION)
    else:
        icon = Image.open(StringIO(self.icon.read()))
        make_thumb(self, icon)
        icon = icon.convert("RGBA")
        img_w, img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        img = img.convert("RGBA")
        img.paste(icon, (w, h), icon)
        img.save(temp_handle, FILE_EXTENSION)
    temp_handle.seek(0)
    suf = SimpleUploadedFile(QR_PATH[-1], temp_handle.read(), content_type=FILE_EXTENSION)
    self.qrmaked.save('qr.%s' % (FILE_EXTENSION), suf, save=False)

def make_thumb(self, icon):
    if not self.icon:
        return
    # icon = Image.open(StringIO(self.icon.read()))
    DJANGO_TYPE = self.icon.file.content_type
    if DJANGO_TYPE == 'image/jpeg':
        PIL_TYPE = 'jpeg'
        FILE_EXTENSION = 'jpg'
    elif DJANGO_TYPE == 'image/png':
        PIL_TYPE = 'png'
        FILE_EXTENSION = 'png'
    temp = StringIO()
    w, h = icon.size
    size = 200
    if w > size or h > size:
        THUMBNAIL_SIZE1 = (size, size)
        thumb = ImageOps.fit(icon, THUMBNAIL_SIZE1, Image.ANTIALIAS)
    else:
        thumb = icon
    thumb.save(temp, PIL_TYPE)
    temp.seek(0)
    suf = SimpleUploadedFile(os.path.split(self.icon.name)[-1], temp.read(), content_type=DJANGO_TYPE)
    self.thumb.save('%s_thumbnail1.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)

class QR(models.Model):
    input = models.TextField(max_length=2000)
    icon = models.ImageField(upload_to=ICON_PATH, height_field=None, width_field=None, max_length=100, null=True, blank=True)
    thumb = models.ImageField(upload_to=QR_PATH, blank=True)
    qrmaked = models.ImageField(upload_to=QR_PATH, blank=True)
    def save(self):
        make_qr(self)
        super(QR, self).save()
    def __unicode__(self):
        return self.input
