from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

def index(r):
    p = Product.objects.all()
    return render(r,'products.html', {'items':p })

def new_product(r,p):
    return HttpResponse("<b>%s</b>" % p)
