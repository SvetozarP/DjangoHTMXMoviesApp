from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('', include('films.urls')),
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
