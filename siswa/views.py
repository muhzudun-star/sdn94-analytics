from django.urls import reverse_lazy

from common.mixins import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Siswa


# ------------------------------------------------------------------
# SISWA
# ------------------------------------------------------------------
class SiswaListView(BaseListView):
    model = Siswa
    title = 'Data Siswa'
    icon = 'bi-people'
    columns = ['NIS', 'NISN', 'Nama', 'Kelas', 'Jenis Kelamin', 'Status']
    create_url_name = 'siswa:siswa_create'
    edit_url_name = 'siswa:siswa_update'
    delete_url_name = 'siswa:siswa_delete'
    row_builder = staticmethod(lambda o: [
        o.nis, o.nisn, o.nama, o.kelas.nama_kelas if o.kelas else '-',
        o.get_jenis_kelamin_display(), o.get_status_display()
    ])


class SiswaCreateView(BaseCreateView):
    model = Siswa
    title = 'Siswa'
    fields = ['nis', 'nisn', 'nama', 'jenis_kelamin', 'tempat_lahir', 'tanggal_lahir',
              'alamat', 'nama_ortu', 'kelas', 'status']
    success_url = reverse_lazy('siswa:siswa_list')


class SiswaUpdateView(BaseUpdateView):
    model = Siswa
    title = 'Siswa'
    fields = ['nis', 'nisn', 'nama', 'jenis_kelamin', 'tempat_lahir', 'tanggal_lahir',
              'alamat', 'nama_ortu', 'kelas', 'status']
    success_url = reverse_lazy('siswa:siswa_list')


class SiswaDeleteView(BaseDeleteView):
    model = Siswa
    title = 'Siswa'
    success_url = reverse_lazy('siswa:siswa_list')
