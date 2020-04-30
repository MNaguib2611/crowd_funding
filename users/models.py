# from django.db import models
# from django_countries.fields import CountryField







from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_countries.fields import CountryField
from .managers import CustomUserManager
# from .forms import User


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    country =  models.CharField(max_length=255)
    picture = models.URLField(null=True)
    fb_page = models.URLField(null=True)

    token      = models.CharField(max_length=255)
    token_date = models.DateTimeField(auto_now=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone','birth_date','country']

    objects = CustomUserManager()

    def __str__(self):
        return "%s %s" % (self.first_name.capitalize(), self.last_name.capitalize())



