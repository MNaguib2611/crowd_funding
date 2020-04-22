from django.shortcuts import render
from django.http import HttpResponse
from .models import User
# Create your views here.

def view_user_profile(request, id):
    user = User.objects.filter(id=id)
    user = user[0]
    user_data = {'user': user}
    return render(request, 'user_profile.html', user_data)
