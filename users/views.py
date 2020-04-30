from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import CustomUser
from projects.models import Donation
from projects.models import Project
from categories.models import Category
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib import messages
# from validate_email import validate_email
#from django.contrib.auth.models  import User, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.forms  import UserCreationForm
from  .models import CustomUser
from django.http.response import HttpResponse
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.models import auth

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django .utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import generate_token 
from django.core.mail import EmailMessage 
from django.conf import  settings
from django.contrib.auth import authenticate, login, logout
from .forms import EditImgForm  
from datetime import datetime , timedelta
from django.utils import timezone



from categories.models import Category
from projects.models import Project, Donation, Report, Tag
from utils.utils import project_is_reported
import re
from django.contrib.auth.decorators import login_required

def email_validator(email):
    if len(email) > 7:
        if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email) is not None:
            return True
    return False

def phone_number_validator(phoneNumber):
    if len(phoneNumber) > 7:
        if re.match("(01)[0-9]{9}", phoneNumber) is not None:
           return True
    return None

def validate_names(fname,lname):

    if fname.isalpha():
        if fname.isalpha():
            return True
    return None

def validate_password(password):
    if re.match("(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$", password):
        return  True
    return None



def signup(request):
    context={
        'data' : request.POST,
        'has error': False
       }
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        picture = request.POST['pic']
        email = request.POST['mail'] 
        password = request.POST['pass'] 
        password2 = request.POST['conf'] 
        phone = request.POST['phone']

        if not validate_names(first_name,last_name):
            messages.add_message(request,messages.ERROR,'please Insert valid Name')
            context['has error'] = True


        
        if not email_validator(email):
            messages.add_message(request,messages.ERROR,'please Insert valid Email')
            context['has error'] = True

        if not phone_number_validator(phone):
            messages.add_message(request,messages.ERROR,'please Insert valid phone Number')
            context['has error'] = True
         
        if password != password2:
            messages.add_message(request,messages.ERROR,'Passwords donot match')
            context['has error'] = True
        

        if not validate_password(password):
            messages.add_message(request,messages.ERROR,'Passwords will contain at least 1 upper case letter,Passwords will contain at least 1 lower case letter , Passwords will contain at least 1 number or special character , Passwords will contain at least 8 characters in length ,Password maximum length should not be arbitrarily limited')
            context['has error'] = True

        


        if not first_name and not last_name and not email and not password and not password2 and not phone:   
           messages.add_message(request,messages.ERROR,'Fields Cannot be blank ') 
        
        
        if context['has error']:
               return render(request,'register.html', context)

        user = User.objects.create_user(password = password, email = email, first_name = first_name, last_name = last_name, phone = phone, picture = picture)
        user.is_active=False
        user_token=generate_token.make_token(user)
        user.token=user_token
        user.save()
        current_site=get_current_site(request)
        email_subject='Activate your Account',
        message=render_to_string('activate.html', 
        {
            'user':user,
            'domain':current_site.domain,
            'uid': user.pk,
            'token':user_token
        })
       
        email_message = EmailMessage(
           email_subject,
           message,
           settings.EMAIL_HOST_USER,
           [email] 
        )
        email_message.send()
        messages.add_message(request,messages.SUCCESS,'Account Created Successfully')
        messages.add_message(request,messages.SUCCESS,'please Activate your Account an Email sent fo Activation')
        print("user Created Successfully") 
        
        # return render(request,'login.html', context) 
        return redirect('login')
    else:            
        return render(request,'register.html', context)  
 
   
#######################SignningIN#############################################


def signin(request):
   if request.user.is_authenticated:
           return redirect('home')
   else:
              if request.method == 'POST':
                    email = request.POST['mail']
                    password =request.POST['pass']
                    user = auth.authenticate(email=email, password=password)
                    print(user)
                    if user is not None:
                        auth.login(request, user)
                        request.session['user_id'] = user.id
                        return redirect('home')
                    else:
                        messages.info(request, 'Username OR Password is incorrect')
                        return render(request, 'login.html')
                        
              else:
                    return render(request, 'login.html')
            #   if request.user.is_authenticated:
            #       return redirect('home')
                    

 #####################Activation##############################################     
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        user=User.objects.get(pk=uidb64)
       
           
        if user and (user.token==token):
            past = timezone.now() - timedelta(days=1)            
            if user.token_date >past:
                user.is_active=True
                user.save()
                messages.add_message(request,messages.SUCCESS,'account activated successfully')
                return redirect('login')
            else:
              messages.info(request, 'Token expired,please request a new token')
              return render(request, 'login.html')  
        return render(request,'activate_failed.html')

##########################Home Page#############################################
@login_required
def home(request):
        return render(request,'home.html')

@login_required
def logOut(request):
        return render(request,'logout.html')




##################################################################################
@login_required
def view_user_profile(request):
    user = CustomUser.objects.filter(id=request.session['user_id'])
    user = user[0]
    form = EditImgForm()
    user_data = {'user': user, 'form': form}
    return render(request, 'users/user_profile.html', user_data)

def edit_photo(request):
    if request.method == "POST":
        if request.FILES['picture']:
            folder = 'users/static/images'
            picture = request.FILES['picture']
            fs = FileSystemStorage(location=folder)
            filename = fs.save(picture.name, picture)
            uploaded_file_url = fs.url(filename)
            photo = uploaded_file_url
            CustomUser.objects.filter(pk=request.session['user_id']).update(picture=photo)
    return redirect(view_user_profile)
    
def edit_name(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        CustomUser.objects.filter(pk=request.session['user_id']).update(first_name=first_name, last_name=last_name)
    return redirect(view_user_profile)
    
def edit_birthdate(request):
    if request.method == "POST":
        birth_date = request.POST['birth_date']
        CustomUser.objects.filter(pk=request.session['user_id']).update(birth_date=birth_date)
    return redirect(view_user_profile)
    

def edit_country(request):
    if request.method == "POST":
        country = request.POST['country']
        CustomUser.objects.filter(pk=request.session['user_id']).update(country=country)
    return redirect(view_user_profile)
    

def edit_password(request):
    if request.method == "POST":
        user = CustomUser.objects.filter(id=request.session['user_id'])
        user = user[0]
        password = request.POST['password']
        user.set_password(password)
        # CustomUser.objects.filter(pk=id).update(password=password)
        user.save()
    return redirect(view_user_profile)
    
def edit_phone(request):
    if request.method == "POST":
        phone = request.POST['phone']
        CustomUser.objects.filter(pk=request.session['user_id']).update(phone=phone)
    return redirect(view_user_profile)
    
def edit_fb_page(request):
    if request.method == "POST":
        fb_page = request.POST['fb_page']
        CustomUser.objects.filter(pk=request.session['user_id']).update(fb_page=fb_page)
    return redirect(view_user_profile)

def delete_account(request):
    # user = CustomUser.objects.filter(id=id)
    # user = user[0]
    # if user.password == request.POST['pass']:   # will be changed and use ajax when using password to delete           
    if request.method == "POST":
        CustomUser.objects.filter(pk=request.session['user_id']).delete()     
    return redirect(signup)   # will be changed----->error here

@login_required
def user_donations(request):
    donations = Donation.objects.filter(user_id=request.session['user_id'])
    projects = Project.objects.all()
    donations_data = {'donations': donations, 'projects': projects}
    return render(request, 'users/user_donations.html', donations_data)

@login_required    
def user_projects(request):
    projects = Project.objects.filter(user_id=request.session['user_id'])
    categories = Category.objects.all()
    projects_data = {'categories': categories, 'projects': projects}
    return render(request, 'users/user_projects.html', projects_data)

def delete_project(request, project_id):
    Project.objects.filter(pk=project_id).delete()
    return redirect(user_projects)
    
@login_required
def edit_project(request, id):
    project = Project.objects.filter(id=id)
    project = project[0]
    categories = Category.objects.all()
    project_data = {'categories': categories, 'project': project}
    return render(request, 'users/edit_project.html', project_data)
    
def update_project(request, project_id):
    if request.method == "POST":
        title = request.POST['title']
        details = request.POST['details']
        target = request.POST['target']
        current = request.POST['current']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        category_id = request.POST['category']
        Project.objects.filter(pk=project_id).update(title=title, details=details, target=target, current=current, 
        start_date=start_date, end_date=end_date, category_id=category_id)
    return redirect(user_projects)
    



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
    user_id = req.session['user_id']
    amount = int(req.POST.get('donation-val'))
    project_id=int(req.POST.get('project_id'))
    user_id=user_id
    print(amount,project_id)
    project = Project.objects.get(id=project_id)
    if project.target - project.current >= amount:
        donation = Donation(project_id=project_id,user_id=user_id,amount=amount)
        donation.save()
        project.current = project.current+amount
        project.save()
    return redirect(req.META.get('HTTP_REFERER'))


def report_project(req,id):
    user_id = req.session['user_id']
    project_id=id
    report = Report(user_id=user_id,project_id=project_id)
    report.save()

    return redirect(req.META.get('HTTP_REFERER'))

def report_comment(req,project_id,comment_id):
    user_id = req.session['user_id']
    report = Report(user_id=user_id,project_id=project_id,comment_id=comment_id)
    report.save()

    return redirect(req.META.get('HTTP_REFERER'))


def search(req):
    search_value = req.GET.get('searchValue')
    projects = Project.objects.filter(Q(tag__tag__icontains=search_value) |  Q(title__icontains=search_value)).distinct().values()
    return JsonResponse(list(projects),safe=False)

def landing(request):
    return redirect('/home')