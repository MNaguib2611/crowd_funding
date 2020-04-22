from django.shortcuts import render
from .models import Project, Report


# Create your views here.


def index(req):
    projects = project_is_reported(Project.objects.all())
    context = {
        'projects':projects
    }
    print("AAA",context)
    # return HttpResponse('<h1>AAAAA</h1>')
    return render(req, 'projects/index.html', context)



def project_is_reported(projects):
    user_id=1
    for project in projects:
        is_reported = Report.objects.filter(project_id=project.id,user_id=user_id).count() != 0
        project.is_reported = is_reported
        # print(is_reported)
    return projects
