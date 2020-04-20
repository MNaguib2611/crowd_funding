import json

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from categories.models import Category
from projects.models import Project
from django.core import serializers


def home(req):
    # print(type(req.GET.get('cat_id')))
    categories = Category.objects.all()
    projects_by_category = get_projects_by_category(req.GET.get('cat_id'))
    paginator_category = Paginator(projects_by_category, 1)  # Show 25 contacts per page.
    page_number = req.GET.get('page_cat')
    page_obj = paginator_category.get_page(page_number)
    context = {
        "projects_by_category":
            {'page_obj': page_obj,
             'projects': page_obj.object_list},
        "categories": {
            "curr_category": int(req.GET.get('cat_id')) if (req.GET.get('cat_id'))  else 0,
            "categories":categories
        }
    }
    print(context)
    return render(req, 'users/home.html',context)


def get_projects_by_category(id):
    if not id or id == '0':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(category_id=int(id))
    return projects
    # return JsonResponse(data)
