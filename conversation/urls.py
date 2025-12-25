from django.urls import path

from . import views

app_name = "conversation"

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('api/create-order/', views.create_order_conversation, name='api_create_order'),
]
