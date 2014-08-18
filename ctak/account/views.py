from django.shortcuts import render, get_object_or_404
from account.models import Producer, Avatar
from django.http import HttpResponseRedirect
from account.userforms import regform, loginform, change_password, AvatarForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
import datetime


@csrf_exempt
def reg(request):
    if request.method == 'POST':
        form = regform(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            p1 = form.cleaned_data['password']
            p2 = form.cleaned_data['password2']
            nn = form.cleaned_data['nickname']
            em = form.cleaned_data['email']
            if User.objects.filter(username=un).exists():
                return render(request, 'account/reg1.html', {'form': form})
            elif p1 != p2 or p1 == '' or p2 == '':
                return render(request, 'account/reg2.html', {'form': form})
            elif Producer.objects.filter(nickname=nn).exists():
                return render(request, 'account/reg3.html', {'form': form})
            else:
                u = User.objects.create_user(username=un, password=p1, email=em)
                p = Producer()
                p.user = u
                p.nickname = nn
                p.save()
                us = authenticate(username=un, password=p1)
                login(request, us)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = regform()

    return render(request, 'account/reg.html', {'form': form})

@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            us = authenticate(username=un, password=pw)
            if not User.objects.filter(username=un).exists():
                return render(request, 'account/login1.html', {'form': form})
            elif us is None:
                return render(request, 'account/login2.html', {'form': form})

            login(request, us)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = loginform()
    return render(request, 'account/login.html', {'form': form})

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@csrf_exempt
@login_required(login_url='/accounts/login/')
def changepassword(request):
    u = request.user
    if request.method == 'POST':
        form = change_password(request.POST)
        if form.is_valid():
            old = form.cleaned_data['old']
            new = form.cleaned_data['new']
            new2 = form.cleaned_data['new2']
            if new != new2 or new == '' or new2 == '':
                return render(request, 'account/change1.html', {'form': form})
            elif authenticate(username=u.username, password=old):
                u.set_password(new)
                u.save()
                return render(request, 'home/success.html', {'form': form})
            else:
                return render(request, 'account/change2.html', {'form': form})

    else:
        form = change_password()
    return render(request, 'account/change.html', {'form': form})

def producer_info(request):
    item = Producer.objects.get(user=request.user)
    if Avatar.objects.filter(owner=item):
        avatar = Avatar.objects.filter(owner=item).order_by('-upload_time')[0]
    else:
        avatar = None
    return render(request, 'account/producer_detail.html', {'item': item, 'avatar': avatar})

class producer_update(UpdateView):
    model = Producer
    fields = ['nickname', 'birthday', 'sex', 'email', 'phone_number', 'introduction']
    template_name_sformfix = '_update_form'
    success_url = reverse_lazy('success')
    def get_object(self):
        return get_object_or_404(self.model, user=self.request.user)

@login_required(login_url='/accounts/login/')
def newavatar(request):
    u = request.user
    item = Producer.objects.get(user=u)
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            i = form.save(commit=False)
            item = Producer.objects.get(user=u)
            i.owner = item
            i.upload_time = datetime.datetime.now()
            i.save()
            return HttpResponseRedirect(reverse('success'))
    else: form = AvatarForm()
    return render(request, 'account/newavatar.html', {'form': form, 'item': item})
