from django.db import models

# Create your models here.
class Category (models.Model):
    name = models.CharField(max_length=255,blank=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % (self.name.capitalize())