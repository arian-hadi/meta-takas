from django.urls import path
from .views import ProductListView, product_detail  # explicitly import function

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', product_detail, name='product_detail'),  # ← changed this line
    path('category/<slug:category_slug>/', ProductListView.as_view(), name='product_list_by_category'),
]
