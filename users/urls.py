from django.urls import path

from users.views import home

urlpatterns = [
    path('home', home,name="home"),
    # path('home/<int:cat_id>', get_projects_by_category,name="get_projects_by_category"),
]