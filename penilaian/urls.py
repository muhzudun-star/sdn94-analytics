from django.urls import path
from . import views

app_name = 'penilaian'

urlpatterns = [
    # Nilai
    path('nilai/', views.NilaiListView.as_view(), name='nilai_list'),
    path('nilai/tambah/', views.NilaiCreateView.as_view(), name='nilai_create'),
    path('nilai/<int:pk>/ubah/', views.NilaiUpdateView.as_view(), name='nilai_update'),
    path('nilai/<int:pk>/hapus/', views.NilaiDeleteView.as_view(), name='nilai_delete'),

    # Kehadiran
    path('kehadiran/', views.KehadiranListView.as_view(), name='kehadiran_list'),
    path('kehadiran/tambah/', views.KehadiranCreateView.as_view(), name='kehadiran_create'),
    path('kehadiran/<int:pk>/ubah/', views.KehadiranUpdateView.as_view(), name='kehadiran_update'),
    path('kehadiran/<int:pk>/hapus/', views.KehadiranDeleteView.as_view(), name='kehadiran_delete'),

    # Prestasi
    path('prestasi/', views.PrestasiListView.as_view(), name='prestasi_list'),
    path('prestasi/tambah/', views.PrestasiCreateView.as_view(), name='prestasi_create'),
    path('prestasi/<int:pk>/ubah/', views.PrestasiUpdateView.as_view(), name='prestasi_update'),
    path('prestasi/<int:pk>/hapus/', views.PrestasiDeleteView.as_view(), name='prestasi_delete'),
]
