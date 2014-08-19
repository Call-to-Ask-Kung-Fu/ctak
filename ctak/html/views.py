from .models import Project
from .forms import ProjectForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ctak.settings import MEDIA_ROOT
from zipfile import ZipFile
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/login/')
def new_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            pn = form.cleaned_data['projectname']
            if Project.objects.filter(projectname=pn).exists():
                return render(request, 'html/new1.html', {'form': form})
            else:
                project = form.save(commit=False)
                project.owner = request.user
                if project.static_zip:
                    project.static_url = 'html/static/%s' % (project.projectname)
                    sta = ZipFile('%s/%s' % (MEDIA_ROOT, project.static_zip))
                    ZipFile.extractall(sta, '%s/%s' % (MEDIA_ROOT, project.static_url))
                project.save()
                return HttpResponseRedirect('%s/' % project.id)
    else: form = ProjectForm()
    return render(request, 'html/new.html', {'form': form})

def detail(request, project_id):
    item = get_object_or_404(Project, pk=project_id)
    context = {'STATIC_PATH' : "/media/" + item.static_url + "/"}
    return render(request, item.template_file, context)  # context)

def listshow(request):
    list1 = Project.objects.all() [:]  # .order_by('-pub_date')[:5]
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
    return render(request, 'html/list.html', context)

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('success')
    def get_object(self, queryset=None):
        obj = super(ProjectDelete, self).get_object()
        u = self.request.user
        if not obj.owner == u:
            raise Http404
        return obj

@login_required(login_url='/account/login/')
def projectmanage(request):
    list1 = Project.objects.filter(owner=request.user)
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
    return render(request, 'html/projectmanage.html', context)
