from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('accounts/', include('accounts.urls')),
    path('info/', include('info.urls')),
    path('products/', include('products.urls')),
    path('contact/', include('contact.urls')),
    path("__reload__/", include("django_browser_reload.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
