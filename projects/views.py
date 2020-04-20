from django.shortcuts import render
from .models import Project
# Create your views here.


def index(req):
    projects = Project.objects.all()
    context = {
        'projects':projects
    }
    print("AAA",context)
    # return HttpResponse('<h1>AAAAA</h1>')
    return render(req, 'projects/index.html', context)

