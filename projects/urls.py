from django.urls import path
from .views import index,launch_project
urlpatterns = [
    path('launch',launch_project,name="launch"),
    path('index', index,name="index"),

]