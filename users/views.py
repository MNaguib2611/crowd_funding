from django.http import HttpResponse
from django.http import JsonResponse
from .models import CustomUser
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import EditImgForm

# Create your views here.
from categories.models import Category
from projects.models import Project, Donation, Report
from utils.utils import project_is_reported

def view_user_profile(request, id):
    user = CustomUser.objects.filter(id=id)
    user = user[0]
    form = EditImgForm()
    user_data = {'user': user, 'form': form}
    return render(request, 'users/user_profile.html', user_data)

def edit_photo(request, id):
    return redirect(view_user_profile, id)
    
def edit_name(request, id):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    CustomUser.objects.filter(pk=id).update(first_name=first_name, last_name=last_name)
    return redirect(view_user_profile, id)
    
def edit_birthdate(request, id):
    birth_date = request.POST['birth_date']
    CustomUser.objects.filter(pk=id).update(birth_date=birth_date)
    return redirect(view_user_profile, id)
    
def edit_country(request, id):
    country = request.POST['country']
    CustomUser.objects.filter(pk=id).update(country=country)
    return redirect(view_user_profile, id)
    
def edit_password(request, id):
    password = request.POST['password']
    CustomUser.objects.filter(pk=id).update(password=password)
    return redirect(view_user_profile, id)
    
def edit_phone(request, id):
    phone = request.POST['phone']
    CustomUser.objects.filter(pk=id).update(phone=phone)
    return redirect(view_user_profile, id)
    
def edit_fb_page(request, id):
    fb_page = request.POST['fb_page']
    CustomUser.objects.filter(pk=id).update(fb_page=fb_page)
    return redirect(view_user_profile, id)

def delete_account(request, id):
    # user = CustomUser.objects.filter(id=id)
    # user = user[0]
    # if user.password == request.POST['pass']:   # will be changed and use ajax when using password to delete           
    CustomUser.objects.filter(pk=id).delete()     
    return redirect(view_user_profile, id)   # will be changed----->error here

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



