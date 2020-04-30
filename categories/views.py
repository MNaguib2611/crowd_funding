from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from categories.models import Category
from django.contrib.auth.decorators import login_required
from crowd_funding import auth

# Create your views here.
@login_required
def index(request):
    if not auth.is_super(request):
        return redirect('login')
        
    categories = Category.objects.all()

    if request.method == "POST":
        if(request.POST['name'] == ''):
            msg = 'You must insert category name!'
            alert = 'danger'
        else:
            category = Category(name = request.POST['name'])
            try:
                category.save()
                msg = 'New category added successfully'
                alert = 'success'
            except IntegrityError as e:
                msg = 'Category already added!'
                alert = 'danger'

        return render(request, 'all.html', { "categories": categories, "msg": msg, "alert": alert })

    else:
        return render(request, 'all.html', { "categories": categories })

def delete(request, id):
    category = Category.objects.get(pk=id)

    if request.method == "GET":
        category.delete()

    if request.method == "POST":
        category.name = request.POST['name']
        category.save()

    return redirect('/admin/category')