from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('nilai', api_views.NilaiViewSet, basename='api-nilai')
router.register('kehadiran', api_views.KehadiranViewSet, basename='api-kehadiran')
router.register('prestasi', api_views.PrestasiViewSet, basename='api-prestasi')

urlpatterns = router.urls
