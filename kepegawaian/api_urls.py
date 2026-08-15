from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('guru', api_views.GuruViewSet, basename='api-guru')

urlpatterns = router.urls
