from django.shortcuts import render

from utils.utils import project_is_reported
from .models import Project, Report


# Create your views here.


def index(req):
    projects = project_is_reported(Project.objects.all())
    context = {
        'projects':projects
    }
    return render(req, 'projects/index.html', context)



