from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('siswa', api_views.SiswaViewSet, basename='api-siswa')

urlpatterns = router.urls
