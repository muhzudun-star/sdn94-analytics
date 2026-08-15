from django.urls import path
from . import views

app_name = 'kepegawaian'

urlpatterns = [
    # Guru
    path('guru/', views.GuruListView.as_view(), name='guru_list'),
    path('guru/tambah/', views.GuruCreateView.as_view(), name='guru_create'),
    path('guru/<int:pk>/ubah/', views.GuruUpdateView.as_view(), name='guru_update'),
    path('guru/<int:pk>/hapus/', views.GuruDeleteView.as_view(), name='guru_delete'),
]
