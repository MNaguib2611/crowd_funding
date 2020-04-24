from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="categories"),
    path('<int:id>', views.delete ,name="delete_category")
]