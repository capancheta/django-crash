from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products'),
    path('<int:p>/', views.new_product, name='new')
]