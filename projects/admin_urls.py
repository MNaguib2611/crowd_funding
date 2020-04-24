from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_projects, name="admin_projects"),
    path('<int:id>', views.admin_delete_projects, name="delete_project"),
]