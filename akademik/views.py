from django.urls import reverse_lazy

from common.mixins import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Kelas, MataPelajaran


# ------------------------------------------------------------------
# KELAS
# ------------------------------------------------------------------
class KelasListView(BaseListView):
    model = Kelas
    title = 'Data Kelas'
    icon = 'bi-door-open'
    columns = ['Nama Kelas', 'Tingkat', 'Tahun Ajaran', 'Wali Kelas']
    create_url_name = 'akademik:kelas_create'
    edit_url_name = 'akademik:kelas_update'
    delete_url_name = 'akademik:kelas_delete'
    row_builder = staticmethod(lambda o: [o.nama_kelas, o.tingkat, o.tahun_ajaran, o.wali_kelas.nama if o.wali_kelas else '-'])


class KelasCreateView(BaseCreateView):
    model = Kelas
    title = 'Kelas'
    fields = ['nama_kelas', 'tingkat', 'tahun_ajaran', 'wali_kelas']
    success_url = reverse_lazy('akademik:kelas_list')


class KelasUpdateView(BaseUpdateView):
    model = Kelas
    title = 'Kelas'
    fields = ['nama_kelas', 'tingkat', 'tahun_ajaran', 'wali_kelas']
    success_url = reverse_lazy('akademik:kelas_list')


class KelasDeleteView(BaseDeleteView):
    model = Kelas
    title = 'Kelas'
    success_url = reverse_lazy('akademik:kelas_list')


# ------------------------------------------------------------------
# MATA PELAJARAN
# ------------------------------------------------------------------
class MapelListView(BaseListView):
    model = MataPelajaran
    title = 'Mata Pelajaran'
    icon = 'bi-journal-bookmark'
    columns = ['Kode', 'Nama Mata Pelajaran', 'KKM']
    create_url_name = 'akademik:mapel_create'
    edit_url_name = 'akademik:mapel_update'
    delete_url_name = 'akademik:mapel_delete'
    row_builder = staticmethod(lambda o: [o.kode_mapel, o.nama_mapel, o.kkm])


class MapelCreateView(BaseCreateView):
    model = MataPelajaran
    title = 'Mata Pelajaran'
    fields = ['kode_mapel', 'nama_mapel', 'kkm']
    success_url = reverse_lazy('akademik:mapel_list')


class MapelUpdateView(BaseUpdateView):
    model = MataPelajaran
    title = 'Mata Pelajaran'
    fields = ['kode_mapel', 'nama_mapel', 'kkm']
    success_url = reverse_lazy('akademik:mapel_list')


class MapelDeleteView(BaseDeleteView):
    model = MataPelajaran
    title = 'Mata Pelajaran'
    success_url = reverse_lazy('akademik:mapel_list')
