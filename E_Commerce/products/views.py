from django.shortcuts import render

# Create your views here.
def product(request):
	return render(request,'product.html')

def categories(request):
	return render(request,'categories.html')

from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def category_page(request, category_id):
	category = get_object_or_404(Category, id=category_id)
	products = Product.objects.filter(category=category)
	return render(request, 'category_page.html', {
'category': category,
'products': products
})