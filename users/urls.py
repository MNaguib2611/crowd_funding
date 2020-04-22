from django.urls import path

from users.views import home,donate, report_project

urlpatterns = [
    path('home', home,name="home"),
    path('donate', donate,name="donate"),
    path('report_project/<int:id>', report_project,name="report_project"),
    # path('home/<int:cat_id>', get_projects_by_category,name="get_projects_by_category"),
]