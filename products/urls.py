from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/', views.product, name='products'),
     path('ajax/search/', views.ajax_product_search, name='ajax_product_search'),
    path('ajax/recommended/<int:product_id>/', views.recommended_products_api, name='recommended_products_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
