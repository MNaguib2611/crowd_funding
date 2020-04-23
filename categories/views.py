from django.db import IntegrityError
from django.shortcuts import redirect
from django.shortcuts import render
from categories.models import Category

# Create your views here.
def index(request):
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
    category.delete()

    return redirect('/admin/category')