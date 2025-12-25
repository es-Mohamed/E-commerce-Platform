# Faster-Parts/cart/urls.py

from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    # path('', views.view_cart, name='view_cart'), # Keep this if you want a dedicated cart page
    path('get_data/', views.get_cart_data, name='get_cart_data'), # New URL for AJAX
    path('update_quantity/<int:item_id>/', views.update_cart_item_quantity, name='update_cart_item_quantity'), # New URL
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'), # New URL
]