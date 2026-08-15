from django.urls import path
from . import views

app_name = 'siswa'

urlpatterns = [
    # Siswa
    path('siswa/', views.SiswaListView.as_view(), name='siswa_list'),
    path('siswa/tambah/', views.SiswaCreateView.as_view(), name='siswa_create'),
    path('siswa/<int:pk>/ubah/', views.SiswaUpdateView.as_view(), name='siswa_update'),
    path('siswa/<int:pk>/hapus/', views.SiswaDeleteView.as_view(), name='siswa_delete'),
]
