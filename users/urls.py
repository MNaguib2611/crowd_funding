from django.urls import path

from users.views import home,donate, report_project, search
from .views import view_user_profile
from users.views import home,donate, report_project

urlpatterns = [
    path('<int:id>', view_user_profile),
    path('home', home,name="home"),
    path('donate', donate,name="donate"),
    path('report_project/<int:id>', report_project,name="report_project"),
    path('search', search,name="search"),
    # path('home/<int:cat_id>', get_projects_by_category,name="get_projects_by_category"),
]