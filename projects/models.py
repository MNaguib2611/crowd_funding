from django.db import models
from users.models import CustomUser as User
from categories.models import Category
from enum import Enum

from datetime import datetime   

   







class Project (models.Model):

    title    = models.CharField(max_length=255)
    details  = models.TextField(max_length=500,null=True)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    target   = models.IntegerField()
    current  = models.IntegerField()
    featured = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "%s" % (self.title)



class Picture (models.Model):
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    picture  = models.TextField()
    def __str__(self):
        return "%s" % (self.picture)




class Tag (models.Model):
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag  = models.CharField(max_length=255)
    def __str__(self):
        return "%s" % (self.tag)


class Donation (models.Model):
    user     = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    project  = models.ForeignKey(Project, on_delete=models.PROTECT)
    amount   = models.IntegerField()
     

class Comment (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment    = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % (self.comment)


class Reply (models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    comment   = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply     =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % (self.reply)


class Report (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    #if comment id is null ->project report
    #if comment id is not null ->comment report
    comment  = models.ForeignKey(Comment, on_delete=models.CASCADE,null=True)
    
   




class Rate (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    rate     =   models.IntegerField()
    def __str__(self):
        return "%s" % (self.rate)        



