from django.urls import path
from . import views

urlpatterns = [
    path('place/', views.place_order, name='place_order'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/track/', views.track_order, name='track_order'),
    path('<int:order_id>/confirm-payment/', views.confirm_payment, name='confirm_payment'),

]
