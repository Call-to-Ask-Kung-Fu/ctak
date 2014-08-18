from django import forms
from account.models import Producer, Avatar
from django.forms import ModelForm

class ProducerForm(ModelForm):
    class Meta:
        model = Producer
        exclude = ['user']

class regform(forms.Form):
    username = forms.CharField()
    nickname = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

class loginform(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class change_password(forms.Form):
    old = forms.CharField(widget=forms.PasswordInput)
    new = forms.CharField(widget=forms.PasswordInput)
    new2 = forms.CharField(widget=forms.PasswordInput)

class AvatarForm(ModelForm):
    class Meta:
        model = Avatar
        exclude = ['owner', 'thumb1', 'thumb2', 'upload_time']

