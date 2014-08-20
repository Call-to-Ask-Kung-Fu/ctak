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
from django.template import RequestContext
import datetime
from ctak.contexts import navcontext


@csrf_exempt
def reg(request):
    if request.method == 'POST':
        form = regform(request.POST)
        context = {'form': form}
        if form.is_valid():
            un = form.cleaned_data['username']
            p1 = form.cleaned_data['password']
            p2 = form.cleaned_data['password2']
            nn = form.cleaned_data['nickname']
            em = form.cleaned_data['email']
            if User.objects.filter(username=un).exists():
                return render(request, 'account/reg1.html', context, context_instance=RequestContext(request, processors=[navcontext]))
            elif p1 != p2 or p1 == '' or p2 == '':
                return render(request, 'account/reg2.html', context)
            elif Producer.objects.filter(nickname=nn).exists():
                return render(request, 'account/reg3.html', context)
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
        context = {'form': form}
    return render(request, 'account/reg.html', context, context_instance=RequestContext(request, processors=[navcontext]))

@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        context = {'form': form}
        if form.is_valid():
            un = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            us = authenticate(username=un, password=pw)
            if not User.objects.filter(username=un).exists():
                return render(request, 'account/login1.html', context, context_instance=RequestContext(request, processors=[navcontext]))
            elif us is None:
                return render(request, 'account/login2.html', context, context_instance=RequestContext(request, processors=[navcontext]))

            login(request, us)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = loginform()
        context = {'form': form}
    return render(request, 'account/login.html', context, context_instance=RequestContext(request, processors=[navcontext]))

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@csrf_exempt
@login_required(login_url='/accounts/login/')
def changepassword(request):

    u = request.user
    if request.method == 'POST':
        form = change_password(request.POST)
        context = {'form': form}
        if form.is_valid():
            old = form.cleaned_data['old']
            new = form.cleaned_data['new']
            new2 = form.cleaned_data['new2']
            if new != new2 or new == '' or new2 == '':
                return render(request, 'account/change1.html', context, context_instance=RequestContext(request, processors=[navcontext]))
            elif authenticate(username=u.username, password=old):
                u.set_password(new)
                u.save()
                return render(request, 'home/success.html', context, context_instance=RequestContext(request, processors=[navcontext]))
            else:
                return render(request, 'account/change2.html', context, context_instance=RequestContext(request, processors=[navcontext]))

    else:
        form = change_password()
        context = {'form': form}
    return render(request, 'account/change.html', context, context_instance=RequestContext(request, processors=[navcontext]))

def producer_info(request, producer_id):
    item = Producer.objects.get(id=producer_id)
    if Avatar.objects.filter(owner=item):
        avatar = Avatar.objects.filter(owner=item).order_by('-upload_time')[0]
    else:
        avatar = None
    context = {'item': item, 'avatar': avatar}
    return render(request, 'account/producer_info.html', context, context_instance=RequestContext(request, processors=[navcontext]))

def producer_detail(request):
    item = Producer.objects.get(user=request.user)
    if Avatar.objects.filter(owner=item):
        avatar = Avatar.objects.filter(owner=item).order_by('-upload_time')[0]
    else:
        avatar = None
    context = {'item': item, 'avatar': avatar}
    return render(request, 'account/producer_detail.html', context, context_instance=RequestContext(request, processors=[navcontext]))

class producer_update(UpdateView):
    model = Producer
    fields = ['nickname', 'birthday', 'sex', 'email', 'phone_number', 'introduction']
    template_name_sformfix = '_update_form'
    success_url = reverse_lazy('success')
    def get_context_data(self, **kwargs):
        context = super(producer_update, self).get_context_data(**kwargs)
        context['navcontext'] = Producer.objects.all()
        return context
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
    context = {'form': form, 'item': item}
    return render(request, 'account/newavatar.html', context, context_instance=RequestContext(request, processors=[navcontext]))
