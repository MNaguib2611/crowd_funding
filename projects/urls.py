from django.urls import path
from .views import index,show,comment,reply,rate,launch_project
urlpatterns = [
    path('<int:project_id>', show ,name="project_show_url"),
    path('launch',launch_project,name="launch"),
    path('index', index,name="index"),
    path('<int:project_id>/rate', rate,name="rate"),
    path('comment', comment,name="comment_url"),
    path('reply', reply,name="reply_url"),
]


