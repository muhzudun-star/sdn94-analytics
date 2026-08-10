from django.urls import path
from . import views

app_name = 'akademik'

urlpatterns = [
    # Guru
    path('guru/', views.GuruListView.as_view(), name='guru_list'),
    path('guru/tambah/', views.GuruCreateView.as_view(), name='guru_create'),
    path('guru/<int:pk>/ubah/', views.GuruUpdateView.as_view(), name='guru_update'),
    path('guru/<int:pk>/hapus/', views.GuruDeleteView.as_view(), name='guru_delete'),

    # Kelas
    path('kelas/', views.KelasListView.as_view(), name='kelas_list'),
    path('kelas/tambah/', views.KelasCreateView.as_view(), name='kelas_create'),
    path('kelas/<int:pk>/ubah/', views.KelasUpdateView.as_view(), name='kelas_update'),
    path('kelas/<int:pk>/hapus/', views.KelasDeleteView.as_view(), name='kelas_delete'),

    # Siswa
    path('siswa/', views.SiswaListView.as_view(), name='siswa_list'),
    path('siswa/tambah/', views.SiswaCreateView.as_view(), name='siswa_create'),
    path('siswa/<int:pk>/ubah/', views.SiswaUpdateView.as_view(), name='siswa_update'),
    path('siswa/<int:pk>/hapus/', views.SiswaDeleteView.as_view(), name='siswa_delete'),

    # Mata Pelajaran
    path('mapel/', views.MapelListView.as_view(), name='mapel_list'),
    path('mapel/tambah/', views.MapelCreateView.as_view(), name='mapel_create'),
    path('mapel/<int:pk>/ubah/', views.MapelUpdateView.as_view(), name='mapel_update'),
    path('mapel/<int:pk>/hapus/', views.MapelDeleteView.as_view(), name='mapel_delete'),

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
