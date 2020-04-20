from django.db import models
from users.models import User
from categories.models import Category


class Project (models.Model):

    title    = models.CharField(max_length=255)
    details  = models.TextField(max_length=500,null=True)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    target   = models.IntegerField()
    current  = models.IntegerField()
    featured = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "%s" % (self.title)



class Picture (models.Model):
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    picture  = models.URLField()
    def __str__(self):
        return "%s" % (self.picture)




class Tag (models.Model):
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag  = models.URLField()
    def __str__(self):
        return "%s" % (self.tag)


class Donation (models.Model):
    user     = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    project  = models.ForeignKey(Project, on_delete=models.PROTECT)
    amount   = models.IntegerField()
     



class Report (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    # type  ->project or comment

class Comment (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment    = models.CharField(max_length=255) 
    def __str__(self):
        return "%s" % (self.comment)


class Rate (models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    project  = models.ForeignKey(Project, on_delete=models.CASCADE)
    rate     =   models.IntegerField()
    def __str__(self):
        return "%s" % (self.rate)        



