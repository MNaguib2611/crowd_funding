from django.urls import path

from users.views import home,donate

urlpatterns = [
    path('home', home,name="home"),
    path('donate', donate,name="donate"),
    # path('home/<int:cat_id>', get_projects_by_category,name="get_projects_by_category"),
]