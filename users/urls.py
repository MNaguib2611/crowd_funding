from django.urls import path
from .views import view_user_profile
from users.views import home,donate, report_project,signin,signup,logOut
from . import views

urlpatterns = [
    path('<int:id>', view_user_profile),
    path('home', home, name="home"),
    path('donate', donate,name="donate"),
    path('report_project/<int:id>', report_project,name="report_project"),
    path('register', signup, name='register'),
    path('login', signin, name='login'),
    path('logout', logOut , name='logout'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate')

    # path('login', views.LoginView.as_view(), name='login')
    
    
    # path('home/<int:cat_id>', get_projects_by_category,name="get_projects_by_category"),
]