from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('kelas', api_views.KelasViewSet, basename='api-kelas')
router.register('mapel', api_views.MataPelajaranViewSet, basename='api-mapel')

urlpatterns = router.urls
