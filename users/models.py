from django.db import models
from django_countries.fields import CountryField




class User (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    picture = models.URLField(null=True)
    fb_page = models.URLField(null=True)
    is_active = models.BooleanField()
    birth_date = models.DateField()
    country = CountryField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)







