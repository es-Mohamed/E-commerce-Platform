from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('', views.Items, name="Items"),
    path('New/', views.New, name="New"),
    path('<int:pk>/', views.Detail, name='Detail'),
    path('<int:pk>/Edit/', views.Edit, name='Edit'),
    path('<int:pk>/delete/', views.delete, name='delete')
]