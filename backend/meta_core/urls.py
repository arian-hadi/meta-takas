from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect
from django.utils import translation

def redirect_to_default_language(request):
    lang = request.session.get('django_language') or request.COOKIES.get('django_language') or 'tr'
    return redirect(f'/{lang}/')

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', redirect_to_default_language),  # <- This redirect fixes root path
]
urlpatterns += i18n_patterns(
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('accounts/', include('accounts.urls')),
    path('info/', include('info.urls')),
    path('products/', include('products.urls')),
    path('contact/', include('contact.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
