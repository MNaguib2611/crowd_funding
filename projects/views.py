from django.shortcuts import render
from django.shortcuts import redirect
from utils.utils import project_is_reported
from .models import Project, Report


# Create your views here.


def index(req):
    projects = project_is_reported(Project.objects.all())
    context = {
        'projects':projects
    }
    return render(req, 'projects/index.html', context)


def admin_projects(request):
    projects = Project.objects.all()

    return render(request, 'projects/admin/all.html', {'projects':projects})

def admin_delete_projects(request, id):
    project = Project.objects.get(pk=id)
    project.delete()

    return redirect('/admin/projects/')