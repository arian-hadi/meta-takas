from django.views.generic import ListView, DetailView
from .models import Product, Category

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'  # you can also name it 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.category_slug = self.kwargs.get('category_slug')  # ← this line is added

        listing_type = self.request.GET.get('type')  # 'sale' or 'exchange'
        
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
        if listing_type in ['sale', 'exchange']:
            queryset = queryset.filter(listing_type=listing_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_slug'] = self.category_slug
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
