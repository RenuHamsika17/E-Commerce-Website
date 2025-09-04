from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_page, name='category_page'),  # ✅ this line
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
