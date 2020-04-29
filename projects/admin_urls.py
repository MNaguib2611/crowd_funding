from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_projects, name="admin_projects"),
    path('<int:id>', views.admin_delete_projects, name="delete_project"),
    path('<int:id>/featured/', views.project_featured, name="project_featured"),
    path('reported_project',views.admin_reported_projects,name="reported_projects"),
    path('reported_project/<int:id>', views.admin_delete_reported_projects, name="delete_reported_project"),
    path('comments/reported/', views.all_reported_comments, name="reported_comments"),
    path('comments/<int:id>', views.delete_comment, name="delete_comment"),
]