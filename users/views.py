from django.http import HttpResponse
from .models import CustomUser
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
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


from categories.models import Category
from projects.models import Project, Donation, Report
from utils.utils import project_is_reported
import re



# Create your views here.
# class RegisterationView(View):
#      def get(self,request):
#         return render(request,'register.html')

#      def post(self, request):
#        context={
#         'data' : request.POST,
#         'has error': False
#        }
#        email = request.POST.get('mail')
#        fname = request.POST.get('fname')
#        lname = request.POST.get('lname')
#        phone = request.POST.get('phone')
#        password = request.POST.get('pass')
#        confpassword = request.POST.get('conf')

#        if len(password)<6:
#           messages.add_message(request,messages.ERROR,'Password should at least 6 characters long ') 
#           context['has error'] = True
#        if password != confpassword:
#           messages.add_message(request,messages.ERROR,'Passwords donot matches')
#           context['has error'] = True
#        if not validate_email(email):
#           messages.add_message(request,messages.ERROR,'please Insert valid Email')
#           context['has error'] = True
#        try:
#             if User.objects.get(email=email):
#               messages.add_message(request,messages.ERROR,'Email is taken')
#               context['has error'] = True
#        except Exception as identifier:
#             pass


#        if context['has error']:
#           return render(request,'register.html', context)
#        user = User.objects.create_user(password = password, email = email, username=fname)
#        user.set_password(password)
#        user.first_name = fname
#        user.last_name =  lname
#        user.email = email
#        user.password = password
#        user.is_active = True

#        user.save()
#        messages.add_message(request,messages.SUCCESS,'Account Created Successfully')
#        return redirect('login')
          
# class LoginView(View):
#     def get(self,request):
#         return render(request,'login.html')
###################################################################################
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
    if re.match("([A-Z][a-zA-Z]*)",fname):
        if re.match("([A-Z][a-zA-Z]*)",lname):
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

        
        # if len(password)<6:
        #     messages.add_message(request,messages.ERROR,'Password should at least 6 characters long ') 
        #     context['has error'] = True

        if not first_name and not last_name and not email and not password and not password2 and not phone:   
           messages.add_message(request,messages.ERROR,'Fields Cannot be blank ') 
        
        
        if context['has error']:
               return render(request,'register.html', context)

        user = User.objects.create_user(password = password, email = email, first_name = first_name, last_name = last_name, phone = phone, picture = picture)
        user.is_active=False
        user.save()
        current_site=get_current_site(request)
        email_subject='Activate your Account',
        message=render_to_string('activate.html', 
        {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
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
        
        return render(request,'login.html', context) 

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
                    if user is not None:
                        auth.login(request, user)
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
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
            print(user)
        except Exception as identifier:
            user=None
           
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            print(user)
            messages.add_message(request,messages.SUCCESS,'account activated successfully')
            return redirect('login')
        return render(request,'activate_failed.html')

##########################Home Page#############################################
def home(request):
        return render(request,'home.html')

def logOut(request):
        return render(request,'logout.html')




##################################################################################
def view_user_profile(request, id):
    user = CustomUser.objects.filter(id=id)
    user = user[0]
    user_data = {'user': user}
    return render(request, 'user_profile.html', user_data)


#def home(req):
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



