from django.urls import path
from . import views

app_name = 'akademik'

urlpatterns = [
    # Kelas
    path('kelas/', views.KelasListView.as_view(), name='kelas_list'),
    path('kelas/tambah/', views.KelasCreateView.as_view(), name='kelas_create'),
    path('kelas/<int:pk>/ubah/', views.KelasUpdateView.as_view(), name='kelas_update'),
    path('kelas/<int:pk>/hapus/', views.KelasDeleteView.as_view(), name='kelas_delete'),

    # Mata Pelajaran
    path('mapel/', views.MapelListView.as_view(), name='mapel_list'),
    path('mapel/tambah/', views.MapelCreateView.as_view(), name='mapel_create'),
    path('mapel/<int:pk>/ubah/', views.MapelUpdateView.as_view(), name='mapel_update'),
    path('mapel/<int:pk>/hapus/', views.MapelDeleteView.as_view(), name='mapel_delete'),
]
