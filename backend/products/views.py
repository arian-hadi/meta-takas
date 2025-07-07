from django.views.generic import ListView, DetailView
from .models import Product, Category, TURKISH_CITIES
from .utils.city_data import CITY_CHOICES, PROVINCE_MAP
from django.db.models import Q, Count
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
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
                Q(exchange_for__name__icontains=search_query) |
                Q(exchange_for__slug__icontains=search_query)
            ).distinct()

        self.category_slug = self.kwargs.get('category_slug')

        province = self.request.GET.get('province')
        selected_categories = self.request.GET.getlist('category')
        selected_types = self.request.GET.getlist('type')
        price_min = self.request.GET.get('min_price')
        price_max = self.request.GET.get('max_price')
        self.sort_by = self.request.GET.get('sort')
        city = self.request.GET.get('city')

        if city:
            queryset = queryset.filter(city=city)

        if province:
            queryset = queryset.filter(province=province) 
 
        if self.category_slug:
            queryset = queryset.filter(category__slug=self.category_slug)

        if selected_categories:
            queryset = queryset.filter(category__slug__in=selected_categories)

        if selected_types:
            queryset = queryset.filter(listing_type__in=selected_types)

        if price_min:
            queryset = queryset.filter(price__gte=price_min)

        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        exchange_for_slugs = self.request.GET.getlist('exchange_for')
        if exchange_for_slugs:
            queryset = queryset.filter(exchange_for__slug__in=exchange_for_slugs).distinct()

        if city:
            queryset = queryset.filter(city=city)

        # Apply sorting
        if self.sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif self.sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif self.sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        elif self.sort_by == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')  # Default: newest first

        return queryset
    

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            products_html = render_to_string(
                'products/product_list.html',
                context,
                request=self.request
            )
            # Extract just the product list section using a unique div ID
            start = products_html.find('<!--PRODUCT-LIST-START-->')
            end = products_html.find('<!--PRODUCT-LIST-END-->')
            only_products = products_html[start + 26:end].strip()
            return JsonResponse({'products_html': only_products})
        
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):   
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        
        listing_type_counts = Product.objects.values('listing_type').annotate(count=Count('id'))
        count_map = {item['listing_type']: item['count'] for item in listing_type_counts}

        types_with_counts = []
        for t in self.types:
            types_with_counts.append({
                'slug': t['slug'],
                'label': t['label'],
                'count': count_map.get(t['slug'], 0)
            })

        
        context['types'] = types_with_counts
        context['current_category_slug'] = self.category_slug

        # Send selected filters back to template
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_types'] = self.request.GET.getlist('type')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['current_sort'] = self.request.GET.get('sort')
        context['search_query'] = self.request.GET.get('q', '')
        context['listing_types'] = self.types
        context['listing_type_counts'] = count_map

        selected_exchange_for = self.request.GET.getlist('exchange_for')
        context['selected_exchange_for'] = selected_exchange_for

        context['cities'] = [city for city, _ in CITY_CHOICES]
        context['selected_city'] = self.request.GET.get('city', '')
        context['selected_province'] = self.request.GET.get('province', '')
        context['province_map'] = PROVINCE_MAP
        context['selected_city'] = self.request.GET.get('city', '')

        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_arg = 'slug'

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).order_by('-id')[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'EXCHANGE_PREFERENCES': Product.EXCHANGE_PREFERENCES,
    })
