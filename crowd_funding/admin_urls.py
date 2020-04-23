from django.urls import path, include

urlpatterns = [
    path('category/', include('categories.urls'))
]