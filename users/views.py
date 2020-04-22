import json

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from categories.models import Category
from projects.models import Project, Donation, Report
from django.core import serializers


def home(req):
    # print(type(req.GET.get('cat_id')))
    categories = Category.objects.all()
    latest_projects = Project.objects.all().order_by('-start_date')[:5]
    paginator_latest_projects = Paginator(latest_projects, 3)  # Show 25 contacts per page.
    page_number_latest_projects = req.GET.get('page_lat_pro')
    page_obj_latest_projects = paginator_latest_projects.get_page(page_number_latest_projects)

    projects_by_category = get_projects_by_category(req.GET.get('cat_id'))
    paginator_category = Paginator(projects_by_category, 3)  # Show 25 contacts per page.
    page_number = req.GET.get('page_cat')
    page_obj = paginator_category.get_page(page_number)

    context = {
        "projects_by_category":
            {'page_obj': page_obj,
             'projects': page_obj.object_list},
        "categories": {
            "curr_category": int(req.GET.get('cat_id')) if (req.GET.get('cat_id'))  else 0,
            "categories":categories
        },
        "latest_projects":
            {'page_obj': page_obj_latest_projects,
             'projects': page_obj_latest_projects.object_list},
    }
    # print(context)
    return render(req, 'users/home.html',context)


def get_projects_by_category(id):
    if not id or id == '0':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(category_id=int(id))
    return projects
    # return JsonResponse(data)

def donate(req):
    amount = int(req.POST.get('donation-val'))
    project_id=int(req.POST.get('project_id'))
    user_id=1
    print(amount,project_id)
    project = Project.objects.get(id=project_id)
    if project.target - project.current >= amount:
        donation = Donation(project_id=project_id,user_id=user_id,amount=amount)
        donation.save()
        project.current = project.current+amount
        project.save()
    return redirect(req.META.get('HTTP_REFERER'))


def report_project(req,id):
    user_id = 1
    project_id=id
    report = Report(user_id=user_id,project_id=project_id)
    report.save()

    return redirect(req.META.get('HTTP_REFERER'))



def project_is_reported(projects):
    user_id=1
    for project in projects:
        is_reported = Report.objects.filter(project_id=project.id,user_id=user_id).count() != 0
        project.is_reported = is_reported
        # print(is_reported)
    return projects