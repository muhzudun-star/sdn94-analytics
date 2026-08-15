from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='analitik:dashboard', permanent=False)),
    path('django-admin/', admin.site.urls),  # admin bawaan django, opsional/cadangan
    path('accounts/', include('accounts.urls')),
    path('data/', include('kepegawaian.urls')),
    path('data/', include('akademik.urls')),
    path('data/', include('siswa.urls')),
    path('data/', include('penilaian.urls')),
    path('analitik/', include('analitik.urls')),
    path('api/', include('kepegawaian.api_urls')),
    path('api/', include('akademik.api_urls')),
    path('api/', include('siswa.api_urls')),
    path('api/', include('penilaian.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
