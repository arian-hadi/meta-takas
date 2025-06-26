from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.db.models import Q, Count
from django.http import JsonResponse
from django.template.loader import render_to_string


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
                Q(exchange_for__icontains=search_query)
            )

        self.category_slug = self.kwargs.get('category_slug')

        selected_categories = self.request.GET.getlist('category')
        selected_types = self.request.GET.getlist('type')
        price_min = self.request.GET.get('min_price')
        price_max = self.request.GET.get('max_price')
        self.sort_by = self.request.GET.get('sort')

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

        # Apply sorting
        if self.sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif self.sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif self.sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-created_at')  # Default

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


        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
