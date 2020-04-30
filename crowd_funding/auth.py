from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def is_super(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return True

    return False
