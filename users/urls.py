from django.urls import path
from .views import view_user_profile

urlpatterns = [
    # path('projects', user_projects,name="user_projects"),
    path('<int:id>', view_user_profile),
]