from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.db.models import Q

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'  # you can also name it 'products/product_list.html'
    context_object_name = 'products'

    types = [
    {'slug': 'sale', 'label': 'Satılık'},
    {'slug': 'exchange', 'label': 'Takas'},
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(exchange_for__icontains=search_query)
    )
        
        self.category_slug = self.kwargs.get('category_slug')  # ← this line is added
        listing_type = self.request.GET.get('type')  # 'sale' or 'exchange'
        self.sort_by = self.request.GET.get('sort')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')


        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)
        
        if listing_type in ['sale', 'exchange']:
            queryset = queryset.filter(listing_type=listing_type)

        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        if price_max:
            queryset = queryset.filter(price__lte=price_max)


        if self.sort_by == 'price_asc':
            # Only apply price sorting to 'sale' products
            if self.listing_type == 'sale':
                queryset = queryset.order_by('price')
        elif self.sort_by == 'price_desc':
            if self.listing_type == 'sale':
                queryset = queryset.order_by('-price')
        elif self.sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-created_at')  # Default: newest
            
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_slug'] = self.category_slug
        context['current_listing_type'] = self.request.GET.get('type')
        context['current_sort'] = self.request.GET.get('sort')
        context['search_query'] = self.request.GET.get('q', '')

        context['types'] = [
        {'slug': 'sale', 'label': 'Satılık'},
        {'slug': 'exchange', 'label': 'Takas'},
        ]

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
