from django.urls import path
from . import views


urlpatterns = [
    path('demo', views.demo, name="django_static_fontawesome.demo"),
]
