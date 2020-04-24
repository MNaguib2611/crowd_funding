from django.urls import path
<<<<<<< HEAD
from .views import index

=======
from .views import index,launch_project
>>>>>>> bb64f3bea83fa2c79de7138bbacba8836932f543
urlpatterns = [
    path('launch',launch_project,name="launch"),
    path('index', index,name="index"),
]