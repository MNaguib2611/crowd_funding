from django.shortcuts import render
from .utils import get_brand_icons
from .utils import get_regular_icons
from .utils import get_solid_icons

def demo(request):
    return render(request, "django_static_fontawesome/demo.html", {
        "brands": get_brand_icons(),
        "regulars": get_regular_icons(),
        "solids": get_solid_icons(),
    })
