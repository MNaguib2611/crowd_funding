from django.urls import path
# from .views import view_user_profile, edit_name
from users.views import view_user_profile, edit_name, edit_birthdate, edit_country, edit_password, edit_phone, edit_fb_page, edit_photo, delete_account, user_donations,user_projects,delete_project,landing

from users.views import home,donate, report_comment,report_project, search,  update_project, edit_project

urlpatterns = [
    path('', landing, name="landing_page"),
    path('delete_project/<int:id> <int:project_id>', delete_project, name="delete_project_url"),
    path('edit_project/<int:id>', edit_project, name="edit_project_url"),
    path('update_project/<int:id> <int:project_id>', update_project, name="update_project_url"),
    path('<int:id>', view_user_profile,name='view_user_profile'),
    path('edit_photo/<int:id>', edit_photo, name="edit_photo_url"),
    path('edit_name/<int:id>', edit_name, name="edit_name_url"),
    path('edit_birthdate/<int:id>', edit_birthdate, name="edit_birthdate_url"),
    path('edit_country/<int:id>', edit_country, name="edit_country_url"),
    path('edit_password/<int:id>', edit_password, name="edit_password_url"),
    path('edit_phone/<int:id>', edit_phone, name="edit_phone_url"),
    path('edit_fb_page/<int:id>', edit_fb_page, name="edit_fb_page_url"),
    path('delete_account/<int:id>', delete_account, name="delete_account_url"),
    path('donations/<int:id>', user_donations, name="user_donations_url"),
    path('projects/<int:id>', user_projects, name="user_projects_url"),
    path('home', home,name="home"),
    path('donate', donate,name="donate"),
    path('report_comment/<int:project_id> <int:comment_id>', report_comment,name="report_comment"),
    path('report_project/<int:id>', report_project,name="report_project"),
    path('search', search,name="search"),
]