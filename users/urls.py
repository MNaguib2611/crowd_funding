from django.urls import path
from . import views
# from users.views import home,donate, report_project,signin,signup,logOut , report_comment,report_project, search 
from users.views import view_user_profile, edit_name, edit_birthdate, edit_country, edit_password, edit_phone, edit_fb_page, edit_photo, delete_account, user_donations,user_projects,delete_project,landing,home,donate, report_project,signin,signup,logOut, search,report_comment

from users.views import home,donate, report_comment,report_project, search, update_project, edit_project

urlpatterns = [
    path('', landing, name="landing_page"),
    path('delete_project/<int:project_id>', delete_project, name="delete_project_url"),
    path('edit_project/<int:id>', edit_project, name="edit_project_url"),
    path('update_project/<int:project_id>', update_project, name="update_project_url"),
    path('profile', view_user_profile,name='view_user_profile'),
    path('edit_photo/', edit_photo, name="edit_photo_url"),
    path('edit_name/', edit_name, name="edit_name_url"),
    path('edit_birthdate/', edit_birthdate, name="edit_birthdate_url"),
    path('edit_country/', edit_country, name="edit_country_url"),
    path('edit_password/', edit_password, name="edit_password_url"),
    path('edit_phone/', edit_phone, name="edit_phone_url"),
    path('edit_fb_page/', edit_fb_page, name="edit_fb_page_url"),
    path('delete_account/', delete_account, name="delete_account_url"),
    path('donations/', user_donations, name="user_donations_url"),
    path('user_projects/', user_projects, name="user_projects_url"),
    path('home', home,name="home"),
    path('donate', donate,name="donate"),
    path('report_comment/<int:project_id> <int:comment_id>', report_comment,name="report_comment"),
    path('report_project/<int:id>', report_project,name="report_project"),
    path('register', signup, name='register'),
    path('login', signin, name='login'),
    path('logout', logOut , name='logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate'),

    # path('login', views.LoginView.as_view(), name='login')
    
    
    # path('home/<int:cat_id>', get_projects_by_category,name="get_projects_by_category"),
    path('search', search,name="search"),
]