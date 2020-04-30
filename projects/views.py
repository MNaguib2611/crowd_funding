from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import JsonResponse
from utils.utils import project_is_reported ,comment_is_reported
from .models import Project, Report, Picture, Tag, Reply,Donation,Rate,Comment
from django.db.models import Avg
from django.db.models import Count
from categories.models import Category
from projects.models import Report, Comment
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from crowd_funding import auth

import math
import time

@login_required
def index(req):
    user_id = req.session['user_id']
    projects = project_is_reported(Project.objects.all(),user_id)
    context = {
        'projects':projects
    }
    return render(req, 'projects/index.html', context)

@login_required
def launch_project(request):
    # print(request.session['user_id'],"AAAA")
    user_id=request.session['user_id'] #will be replaced by logged user

    if request.method.lower() == "get":
        categories= Category.objects.filter()
        context={"categories":categories} 
        return render(request,"projects/launch_project.html",context)
    elif request.method.lower() =="post":
        try:
            if time.strptime(  request.POST["end_date"] , '%Y-%m-%d') or time.strptime(  request.POST["start_date"] , '%Y-%m-%d'):
                if request.POST["end_date"] < request.POST["start_date"] or request.POST["end_date"] =='' or request.POST["start_date"]=='': 
                    msg = 'You must insert project start data proceeding end data !'
                    alert = 'danger'
                elif(request.POST['title'] == '' or request.POST['target']=='' or request.POST['current']==''):
                    msg = 'You must insert project Data!'
                    alert = 'danger'
                
                else:
                    try:
                    
                        title = request.POST["title"]
                        # category = request.FILES.get("category")
                        category = request.POST["category"]
                        print (category)

                        details = request.POST["details"]
                        target = request.POST["target"]
                        current = request.POST["current"]
                        # featured = request.POST["featured"]
                        start_date = request.POST["start_date"]
                        end_date = request.POST["end_date"]
                        # pictures = request.FILES.getlist("picture[]",None)
                        # picture=request.FILES.get('picture', None)
                        cat=Category.objects.get(pk=category)
                        print (cat)
                        # user=User.objects.get(pk=1)

                        msg = 'New project added successfully'
                        alert = 'success'
                        project_instance=Project.objects.create(featured=0,end_date=end_date,start_date=start_date,
                        title=title,details=details,target=target,current=current
                        ,category=cat,user_id=user_id
                        )
                       
                        for picture in request.FILES.getlist("picture[]",None):
                            if picture is not None and picture != '':
                                from django.core.files.storage import FileSystemStorage
                                fs = FileSystemStorage(location='projects/static/images')
                                filename = fs.save(picture.name, picture)
                                uploaded_file_url = fs.url(filename)
                                picture_instance=Picture.objects.create(picture=picture,project=project_instance)
                        
                        searchForValue = ','
                        tag = request.POST["tag"]
                        if tag is not None and tag != '':
                            if searchForValue in tag:
                                tags=tag.split(',')
                                for tag in tags:
                                    if tag is not None and tag != '':
                                        tag_instance=Tag.objects.create(tag=tag,project=project_instance)       
                            else:    
                                tag_instance=Tag.objects.create(tag=tag,project=project_instance)
                

                    except IntegrityError as e:
                        print(e)
                        msg = 'project already added!'
                        alert = 'danger'

        
       
        except ValueError:
                msg='Invalild Date Format'
                alert='danger' 
        projects= Project.objects.filter()
        categories= Category.objects.filter()
        context={"projects":projects,"categories":categories,"msg": msg, "alert": alert,
     
        } 
        return render(request,"projects/launch_project.html",context) 

@login_required
def admin_projects(request):
    if not auth.is_super(request):
        return redirect('login')

    projects = Project.objects.all()

    return render(request, 'projects/admin/all.html', {'projects':projects})

@login_required
def admin_reported_projects(request):
    if not auth.is_super(request):
        return redirect('login')

    user_id=request.session['user_id']
    projects=[]
    distinct = Report.objects.values(
    'project_id'
    ).annotate(
        name_count=Count('project_id')
    )
    # print(distinct)

    not_commented=distinct.filter(comment_id__isnull = True)
    # print(not_commented)

    if Report.objects.filter(comment_id__isnull = True) :
        projects = Project.objects.filter(id__in=[item['project_id'] for item in not_commented ])
        # print(projects)
    # reported_projects = Report.objects.distinct()
    # for reported_project in reported_projects:
    #     if reported_project.comment_id == None :
    #         projects += Project.objects.filter(id=reported_project.project_id)
            
    context = {'projects':projects}
    return render(request, 'projects/admin/reported_projects.html', context )
    
# def admin_delete_reported_projects(request, id):
    # # project = Project.objects.get(pk=id)
    # # project.delete()
    # return redirect('/admin/projects/reported_project')
def admin_delete_reported_projects(request, id):
    if not auth.is_super(request):
        return redirect('login')

    project = Project.objects.get(pk=id)
    # if (project_donation):
    #     project_donation.delete()
    #     project.delete()
    project_donations,created=Donation.objects.get_or_create(project=project,amount=0)
    print(project_donations)
    project_donation=Donation.objects.filter(project=id)
    if len(project_donation) is 1 and created==True:
        project_donation.delete()
        project.delete()
    elif len(project_donation) is 1 and created==False:
        project_donation.update(project=None)
        project.delete()    
    elif  len(project_donation)>1 :
        project_donation.update(project=None)
        project.delete()
    return redirect('/admin/projects/reported_project')

def admin_delete_projects(request, id):
    project = Project.objects.get(pk=id)
    project.delete()
    return redirect('/admin/projects/')

@login_required
def project_featured(request, id):
    if not auth.is_super(request):
        return redirect('login')

    project = Project.objects.get(pk=id)
    if(project.featured == 1):
        project.featured = 0
    else:
        project.featured = 1
    
    
    project.save()

    return JsonResponse({'status':200})

@login_required
def show(request,project_id):
    user_id=request.session['user_id'] #will be replaced by logged user
    project_data  = Project.objects.get(id=project_id)
    pictures_data = Picture.objects.filter(project_id=project_id)
    is_reported=Report.objects.filter(project_id=project_id,user_id=user_id);
    comments = comment_is_reported(Comment.objects.filter(project_id=project_id),user_id)
    tags=project_data.tag_set.filter(project_id=project_id).values('tag')
    project_ids=Tag.objects.filter(tag__in=tags).exclude(project_id =project_id).values('project_id')
    print(project_ids)
    projects = Project.objects.filter(id__in=project_ids)[0:5]
    try:
        user_rate = Rate.objects.get(project_id=project_id,user_id=user_id)
        user_rate_val=f"you rated this project { user_rate }"
    except Rate.DoesNotExist:
        user_rate = None
        user_rate_val=f"you haven't rated this project yet"


    avg_rating_dict=Rate.objects.filter(project_id=project_id).aggregate(Avg('rate'))
    if avg_rating_dict['rate__avg']:
        avg_rating= math.floor(float(avg_rating_dict['rate__avg'])*10)/10
    else:
        avg_rating=0



    context={
        'projects' : projects,
        'project'  : project_data,
        'time'     :  project_data.end_date < datetime.now().date(),
        'pictures'  : pictures_data,
        'reported' : is_reported,
        'comments' : comments,
        'user_rate_val': user_rate_val,
        'rating'   : avg_rating ,
        'rating_f' : int( ( avg_rating-int(avg_rating) )*10 ),
        'rating_i' : range(int(avg_rating)),
        }
    return render(request, 'projects/show.html', context)

def comment(req):
    user_id=req.session['user_id']
    new_comment=Comment(
                comment=req.POST['comment'],
                project_id=req.POST['project_id'],
                user_id=user_id
                )
    new_comment.save()            
    return redirect(f"/projects/{req.POST['project_id'] }" )            

def reply(req):
    user_id = req.session['user_id']
    user_id=user_id
    new_reply=Reply(
                reply=req.POST['reply'],
                comment_id=req.POST['comment_id'],
                user_id=user_id
                )
    new_reply.save()  
    print (new_reply.comment)
        
    return redirect(f"/projects/{new_reply.comment.project.id }" )   


def rate(req,project_id):
    user_id = req.session['user_id']
    try:
        rate_exists = Rate.objects.get(project_id=project_id,user_id=user_id)
    except Rate.DoesNotExist:
        rate_exists = None
    if rate_exists:
        rate_exists.rate=req.GET['rate_val']
        rate_exists.save()
        response_message=["Rate has been updated"]
    else:
        new_rate = Rate(project_id=project_id,user_id=user_id,rate=req.GET['rate_val'])
        new_rate.save()
    return redirect(f"/projects/{project_id}" )  

@login_required
def all_reported_comments(request):
    if not auth.is_super(request):
        return redirect('login')

    all_reports = Report.objects.exclude(comment_id=None)
    reports = [all_reports.filter(comment_id=item['comment_id']).last() for item in Report.objects.values('comment_id').distinct()]
    return render(request, 'projects/admin/reported_comments.html', {'reports': reports} )

def delete_comment(request, id):
    if not auth.is_super(request):
        return redirect('login')

    report = Report.objects.get(pk=id)
    comment = Comment.objects.get(pk=report.comment_id)
    comment.delete()
    report.delete()

    return redirect('/admin/projects/comments/reported/')