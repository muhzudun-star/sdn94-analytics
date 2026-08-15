from django.urls import reverse_lazy

from common.mixins import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Nilai, Kehadiran, Prestasi


# ------------------------------------------------------------------
# NILAI
# ------------------------------------------------------------------
class NilaiListView(BaseListView):
    model = Nilai
    title = 'Data Nilai'
    icon = 'bi-clipboard-data'
    columns = ['Siswa', 'Mapel', 'Jenis', 'Nilai', 'Semester', 'Tahun Ajaran']
    create_url_name = 'penilaian:nilai_create'
    edit_url_name = 'penilaian:nilai_update'
    delete_url_name = 'penilaian:nilai_delete'
    row_builder = staticmethod(lambda o: [
        o.siswa.nama, o.mapel.nama_mapel, o.get_jenis_nilai_display(),
        o.nilai, o.get_semester_display(), o.tahun_ajaran
    ])


class NilaiCreateView(BaseCreateView):
    model = Nilai
    title = 'Nilai'
    fields = ['siswa', 'mapel', 'jenis_nilai', 'nilai', 'semester', 'tahun_ajaran']
    success_url = reverse_lazy('penilaian:nilai_list')


class NilaiUpdateView(BaseUpdateView):
    model = Nilai
    title = 'Nilai'
    fields = ['siswa', 'mapel', 'jenis_nilai', 'nilai', 'semester', 'tahun_ajaran']
    success_url = reverse_lazy('penilaian:nilai_list')


class NilaiDeleteView(BaseDeleteView):
    model = Nilai
    title = 'Nilai'
    success_url = reverse_lazy('penilaian:nilai_list')


# ------------------------------------------------------------------
# KEHADIRAN
# ------------------------------------------------------------------
class KehadiranListView(BaseListView):
    model = Kehadiran
    title = 'Data Kehadiran'
    icon = 'bi-calendar-check'
    columns = ['Siswa', 'Tanggal', 'Status', 'Keterangan']
    create_url_name = 'penilaian:kehadiran_create'
    edit_url_name = 'penilaian:kehadiran_update'
    delete_url_name = 'penilaian:kehadiran_delete'
    row_builder = staticmethod(lambda o: [o.siswa.nama, o.tanggal, o.get_status_display(), o.keterangan])


class KehadiranCreateView(BaseCreateView):
    model = Kehadiran
    title = 'Kehadiran'
    fields = ['siswa', 'tanggal', 'status', 'keterangan']
    success_url = reverse_lazy('penilaian:kehadiran_list')


class KehadiranUpdateView(BaseUpdateView):
    model = Kehadiran
    title = 'Kehadiran'
    fields = ['siswa', 'tanggal', 'status', 'keterangan']
    success_url = reverse_lazy('penilaian:kehadiran_list')


class KehadiranDeleteView(BaseDeleteView):
    model = Kehadiran
    title = 'Kehadiran'
    success_url = reverse_lazy('penilaian:kehadiran_list')


# ------------------------------------------------------------------
# PRESTASI
# ------------------------------------------------------------------
class PrestasiListView(BaseListView):
    model = Prestasi
    title = 'Data Prestasi'
    icon = 'bi-trophy'
    columns = ['Siswa', 'Nama Prestasi', 'Tingkat', 'Tahun']
    create_url_name = 'penilaian:prestasi_create'
    edit_url_name = 'penilaian:prestasi_update'
    delete_url_name = 'penilaian:prestasi_delete'
    row_builder = staticmethod(lambda o: [o.siswa.nama, o.nama_prestasi, o.get_tingkat_display(), o.tahun])


class PrestasiCreateView(BaseCreateView):
    model = Prestasi
    title = 'Prestasi'
    fields = ['siswa', 'nama_prestasi', 'tingkat', 'tahun', 'keterangan']
    success_url = reverse_lazy('penilaian:prestasi_list')


class PrestasiUpdateView(BaseUpdateView):
    model = Prestasi
    title = 'Prestasi'
    fields = ['siswa', 'nama_prestasi', 'tingkat', 'tahun', 'keterangan']
    success_url = reverse_lazy('penilaian:prestasi_list')


class PrestasiDeleteView(BaseDeleteView):
    model = Prestasi
    title = 'Prestasi'
    success_url = reverse_lazy('penilaian:prestasi_list')
