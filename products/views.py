from django.shortcuts import render
from .models import Product  # make sure Product model is imported
# Create your views here.def product(request)

def product(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

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

def product_detail(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	return render(request, 'product_detail.html', {'product': product})

from django.shortcuts import render
from .models import Product
from django.db.models import Q
from django.http import JsonResponse


# AJAX Search View
def ajax_product_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'image_url': product.image.url if product.image else '/static/images/placeholder.png',
                'url': f'/product/{product.id}/',
            })

    return JsonResponse({'results': results})


# Optional: Separate recommended API if needed
def recommended_products_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recommended = Product.objects.filter(category=product.category).exclude(id=product.id)[:10]

    data = [
        {
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'image_url': p.image.url,
            'url': f'/product/{p.id}/',
        }
        for p in recommended
    ]

    return JsonResponse({'products': data})

