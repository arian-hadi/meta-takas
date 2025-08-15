from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import set_language           # ✅ for the set_language view
from django.conf.urls.i18n import i18n_patterns      # ✅ for i18n_patterns
from django.shortcuts import redirect


# Redirect users to their preferred language
def redirect_to_default_language(request):
    lang = request.session.get('django_language') or request.COOKIES.get('django_language') or 'tr'
    return redirect(f'/{lang}/')

# 🌍 NON-TRANSLATED ROUTES (must be outside i18n_patterns)
urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),  # ✅ Explicitly registered
    path('i18n/', include('django.conf.urls.i18n')),           # Optional: includes other i18n views
    path('', redirect_to_default_language),
]

# 🌍 TRANSLATED ROUTES
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),
    path('', include('homepage.urls')),
    path('accounts/', include('accounts.urls')),
    path('info/', include('info.urls')),
    path('products/', include('products.urls')),
    path('contact/', include('contact.urls')),
)

# 🌐 Static/media serving in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
