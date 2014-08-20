from django.shortcuts import render
from ctak.contexts import navcontext
from django.template import RequestContext
from .models import Index
from .forms import IndexForm
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from account.models import Producer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'home/home.html', context_instance=RequestContext(request, processors=[navcontext]))

def success(request):
    return render(request, 'home/success.html', context_instance=RequestContext(request, processors=[navcontext]))

@login_required(login_url='/account/login/')
def newindex(request):
    if request.method == 'POST':
        form = IndexForm(request.POST, request.FILES)
        if form.is_valid():
            pn = form.cleaned_data['project']
            if Index.objects.filter(project=pn).exists():
                return render(request, 'ctak/new1.html', {'form': form}, context_instance=RequestContext(request, processors=[navcontext]))
            else:
                i = form.save(commit=False)
                p = Producer.objects.get(user=request.user)
                i.owner = p
                i.type = 'Django'
                i.save()
                return HttpResponseRedirect('/')
    else: form = IndexForm()
    return render(request, 'ctak/new.html', {'form': form}, context_instance=RequestContext(request, processors=[navcontext]))

class IndexDelete(DeleteView):
    model = Index
    success_url = reverse_lazy('success')
    def get_object(self, queryset=None):
        obj = super(IndexDelete, self).get_object()
        u = self.request.user
        p = Producer.objects.get(user=u)
        if not obj.owner == p:
            raise Http404
        return obj
    def get_context_data(self, **kwargs):
        context = super(IndexDelete, self).get_context_data(**kwargs)
        context['navcontext'] = Producer.objects.all()
        return context

@login_required(login_url='/account/login/')
def indexmanage(request):
    p = Producer.objects.get(user=request.user)
    list1 = Index.objects.filter(owner=p, type='Django')
    paginator = Paginator(list1, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    context = {'items': items}
    return render(request, 'ctak/indexmanage.html', context, context_instance=RequestContext(request, processors=[navcontext]))
