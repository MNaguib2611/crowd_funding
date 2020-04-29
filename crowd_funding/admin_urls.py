from django.urls import path, include

urlpatterns = [
    path('category/', include('categories.urls')),
    path('projects/', include('projects.admin_urls')),
]