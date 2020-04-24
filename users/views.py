from django.http import HttpResponse
from .models import CustomUser
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime


# Create your views here.
from categories.models import Category
from projects.models import Project, Donation, Report, Tag
from utils.utils import project_is_reported

def view_user_profile(request, id):
    user = CustomUser.objects.filter(id=id)
    user = user[0]
    user_data = {'user': user}
    return render(request, 'user_profile.html', user_data)


def home(req):
    categories = Category.objects.all()

    latest_projects = project_is_reported(Project.objects.all().order_by('-start_date')[:5])
    paginator_latest_projects = Paginator(latest_projects, 3)  # Show 25 contacts per page.
    page_number_latest_projects = req.GET.get('page_lat_pro')
    page_obj_latest_projects = paginator_latest_projects.get_page(page_number_latest_projects)

    projects_by_category = project_is_reported(get_projects_by_category(req.GET.get('cat_id')))
    paginator_category = Paginator(projects_by_category, 3)  # Show 25 contacts per page.
    page_number = req.GET.get('page_cat')
    page_obj = paginator_category.get_page(page_number)

    latest_featured_projects = project_is_reported(Project.objects.filter(featured=1).order_by('-start_date')[:5])
    paginator_latest_featured_projects = Paginator(latest_featured_projects, 3)  # Show 25 contacts per page.
    page_number_latest_featured_projects = req.GET.get('page_latest_featured_project')
    page_obj_latest_featured_projects = paginator_latest_featured_projects.get_page(page_number_latest_featured_projects)

    highest_rated_projects = project_is_reported(Project.objects.filter(end_date__gt=datetime.now()).annotate(rate_avg=Avg('rate__rate')).order_by('-rate_avg')[:5])
    print(highest_rated_projects)
    paginator_highest_rated_projects = Paginator(highest_rated_projects, 3)  # Show 25 contacts per page.
    page_number_highest_rated_projects = req.GET.get('page_highest_rated_projects')
    page_obj_highest_rated_projects = paginator_highest_rated_projects.get_page(
        page_number_highest_rated_projects)

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
        "page_obj_latest_featured_projects":
            {'page_obj': page_obj_latest_featured_projects,
             'projects': page_obj_latest_featured_projects.object_list},
        "highest_rated_projects":
            {'page_obj': page_obj_highest_rated_projects,
             'projects': page_obj_highest_rated_projects.object_list},
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

def report_comment(req,project_id,comment_id):
    user_id = 1
    report = Report(user_id=user_id,project_id=project_id,comment_id=comment_id)
    report.save()

    return redirect(req.META.get('HTTP_REFERER'))


def search(req):
    search_value = req.GET.get('searchValue')
    projects = Project.objects.filter(Q(tag__tag__icontains=search_value) |  Q(title__icontains=search_value)).distinct().values()
    return JsonResponse(list(projects),safe=False)
