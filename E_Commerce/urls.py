"""
URL configuration for E_Commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views
from users import views as user_views
from products import views as product_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
path('admin/', admin.site.urls),
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('contact/', views.contact, name='contact'),
path('signup/', user_views.signup_view, name='signup'),
path('login/', user_views.login_view, name='login'),
path('logout/', user_views.logout_view, name='logout'),
path('', include('products.urls')),# ✅ this handles category/int:id from products.urls
path('dashboard/', user_views.dashboard_view, name='dashboard'),
path('edit-profile/', user_views.edit_profile, name='edit_profile'),
path('add/', user_views.add_product, name='add_product'),
path('cart/', include('cart.urls')),
path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
path('orders/', include('orders.urls')),
path('product/<int:product_id>/', product_views.product_detail, name='product_detail'),
path('category/<int:category_id>/', product_views.category_page, name='category_page'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)