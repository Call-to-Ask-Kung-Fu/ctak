from .forms import QRForm
from django.http import HttpResponseRedirect
from .models import QR
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ctak.contexts import navcontext
from django.template import RequestContext

def Create(request):
    if request.method == 'POST':
        form = QRForm(request.POST, request.FILES)
        if form.is_valid():
            qr = form.save()
            return HttpResponseRedirect('%s/' % qr.id)
    else: form = QRForm()
    return render(request, 'qrmaker/qr.html', {'form': form}, context_instance=RequestContext(request, processors=[navcontext]))

def detail(request, qr_id):
    item = get_object_or_404(QR, pk=qr_id)
    return render(request, 'qrmaker/detail.html', {'item': item}, context_instance=RequestContext(request, processors=[navcontext]))

def listshow(request):
    list1 = QR.objects.all() [:]  # .order_by('-pub_date')[:5]
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
    return render(request, 'qrmaker/list.html', context, context_instance=RequestContext(request, processors=[navcontext]))

# Create your views here.
