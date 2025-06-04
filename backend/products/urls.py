from django.urls import path
from .views import *


urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
]