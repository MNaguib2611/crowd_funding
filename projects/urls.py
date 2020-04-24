from django.urls import path
from .views import index,show,comment,rate
urlpatterns = [
    path('<int:project_id>', show ,name="project_show_url"),
    path('index', index,name="index"),
    path('<int:project_id>/rate', rate,name="rate"),
    path('comment', comment,name="comment_url"),
]