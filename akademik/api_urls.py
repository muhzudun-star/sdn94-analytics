from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('guru', api_views.GuruViewSet, basename='api-guru')
router.register('kelas', api_views.KelasViewSet, basename='api-kelas')
router.register('siswa', api_views.SiswaViewSet, basename='api-siswa')
router.register('mapel', api_views.MataPelajaranViewSet, basename='api-mapel')
router.register('nilai', api_views.NilaiViewSet, basename='api-nilai')
router.register('kehadiran', api_views.KehadiranViewSet, basename='api-kehadiran')
router.register('prestasi', api_views.PrestasiViewSet, basename='api-prestasi')

urlpatterns = router.urls
