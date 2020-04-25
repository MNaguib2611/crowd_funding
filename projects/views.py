from django.shortcuts import render

from utils.utils import project_is_reported
from .models import Project, Report,Picture,Tag
from categories.models import Category

# import os
# from flask import Flask, flash, request, redirect, url_for
from flask import Flask
# from app.forms import Image/

# from werkzeug.utils import secure_filename

# Create your views here.

# @app.route("projects/launch_project.html", methods=["POST"])

def index(req):
    projects = project_is_reported(Project.objects.all())
    context = {
        'projects':projects
    }
    return render(req, 'projects/index.html', context)



def launch_project(request):
    if request.method.lower() == "get":
      return render(request,"projects/launch_project.html")
    elif request.method.lower() =="post":
        title = request.POST["title"]
        # category = request.POST["category"]
        details = request.POST["details"]
        target = request.POST["target"]
        current = request.POST["current"]
        # featured = request.POST["featured"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        # pictures = request.FILES.getlist("picture[]",None)
        # print uploaded_files
        # picture=request.FILES.get('picture', None)

        project_instance=Project.objects.create(featured=0,end_date=end_date,start_date=start_date,
        title=title,details=details,target=target,current=current
        # ,category=category
        )
        for picture in request.FILES.getlist("picture[]",None):
            if picture is not None and picture != '':
                picture_instance=Picture.objects.create(picture=picture,project=project_instance)
        
        searchForValue = ','
        tag = request.POST["tag"]
        if tag is not None and tag != '':
            if searchForValue in tag:
                tags=tag.split(',')
                for tag in tags:
                    tag_instance=Tag.objects.create(tag=tag,project=project_instance)       
            else:    
                tag_instance=Tag.objects.create(tag=tag,project=project_instance)
        

        projects= Project.objects.filter()
        categories= Category.objects.filter()

        context={"projects":projects,"categories":categories} 
        return render(request,"projects/launch_project.html",context)
