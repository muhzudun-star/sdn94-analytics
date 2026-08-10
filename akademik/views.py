from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .models import Guru, Kelas, Siswa, MataPelajaran, Nilai, Kehadiran, Prestasi


class AdminRequiredMixin(UserPassesTestMixin):
    """Hanya user dengan role ADMIN (atau superuser) yang boleh mengelola data master."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        profile = getattr(user, 'profile', None)
        return bool(user.is_superuser or (profile and profile.is_admin_role))

    def handle_no_permission(self):
        messages.error(self.request, "Anda tidak memiliki akses untuk mengelola data ini.")
        from django.shortcuts import redirect
        return redirect('analitik:dashboard')


class BaseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    paginate_by = 15
    template_name = 'akademik/crud_list.html'
    title = ''
    columns = []       # list of header string
    row_builder = None  # function(obj) -> list of cell string
    create_url_name = ''
    edit_url_name = ''
    delete_url_name = ''
    icon = 'bi-table'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        rows = []
        for obj in ctx['object_list']:
            rows.append({
                'pk': obj.pk,
                'cells': self.row_builder(obj) if self.row_builder else [str(obj)],
            })
        ctx.update({
            'title': self.title,
            'columns': self.columns,
            'rows': rows,
            'create_url_name': self.create_url_name,
            'edit_url_name': self.edit_url_name,
            'delete_url_name': self.delete_url_name,
            'icon': self.icon,
        })
        return ctx


class BaseCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = 'akademik/crud_form.html'
    title = ''
    icon = 'bi-plus-circle'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Tambah {self.title}"
        ctx['icon'] = self.icon
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"{self.title} berhasil ditambahkan.")
        return super().form_valid(form)


class BaseUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = 'akademik/crud_form.html'
    title = ''
    icon = 'bi-pencil-square'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = f"Ubah {self.title}"
        ctx['icon'] = self.icon
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"{self.title} berhasil diperbarui.")
        return super().form_valid(form)


class BaseDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    template_name = 'akademik/crud_confirm_delete.html'
    title = ''

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.title
        return ctx

    def form_valid(self, form):
        messages.success(self.request, f"{self.title} berhasil dihapus.")
        return super().form_valid(form)


# ------------------------------------------------------------------
# GURU
# ------------------------------------------------------------------
class GuruListView(BaseListView):
    model = Guru
    title = 'Data Guru'
    icon = 'bi-person-badge'
    columns = ['NIP', 'Nama', 'Jenis Kelamin', 'No. HP', 'Alamat']
    create_url_name = 'akademik:guru_create'
    edit_url_name = 'akademik:guru_update'
    delete_url_name = 'akademik:guru_delete'
    row_builder = staticmethod(lambda o: [o.nip, o.nama, o.get_jenis_kelamin_display(), o.no_hp, o.alamat])


class GuruCreateView(BaseCreateView):
    model = Guru
    title = 'Guru'
    fields = ['nip', 'nama', 'jenis_kelamin', 'no_hp', 'alamat', 'tanggal_bergabung']
    success_url = reverse_lazy('akademik:guru_list')


class GuruUpdateView(BaseUpdateView):
    model = Guru
    title = 'Guru'
    fields = ['nip', 'nama', 'jenis_kelamin', 'no_hp', 'alamat', 'tanggal_bergabung']
    success_url = reverse_lazy('akademik:guru_list')


class GuruDeleteView(BaseDeleteView):
    model = Guru
    title = 'Guru'
    success_url = reverse_lazy('akademik:guru_list')


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
# SISWA
# ------------------------------------------------------------------
class SiswaListView(BaseListView):
    model = Siswa
    title = 'Data Siswa'
    icon = 'bi-people'
    columns = ['NIS', 'NISN', 'Nama', 'Kelas', 'Jenis Kelamin', 'Status']
    create_url_name = 'akademik:siswa_create'
    edit_url_name = 'akademik:siswa_update'
    delete_url_name = 'akademik:siswa_delete'
    row_builder = staticmethod(lambda o: [
        o.nis, o.nisn, o.nama, o.kelas.nama_kelas if o.kelas else '-',
        o.get_jenis_kelamin_display(), o.get_status_display()
    ])


class SiswaCreateView(BaseCreateView):
    model = Siswa
    title = 'Siswa'
    fields = ['nis', 'nisn', 'nama', 'jenis_kelamin', 'tempat_lahir', 'tanggal_lahir',
              'alamat', 'nama_ortu', 'kelas', 'status']
    success_url = reverse_lazy('akademik:siswa_list')


class SiswaUpdateView(BaseUpdateView):
    model = Siswa
    title = 'Siswa'
    fields = ['nis', 'nisn', 'nama', 'jenis_kelamin', 'tempat_lahir', 'tanggal_lahir',
              'alamat', 'nama_ortu', 'kelas', 'status']
    success_url = reverse_lazy('akademik:siswa_list')


class SiswaDeleteView(BaseDeleteView):
    model = Siswa
    title = 'Siswa'
    success_url = reverse_lazy('akademik:siswa_list')


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


# ------------------------------------------------------------------
# NILAI
# ------------------------------------------------------------------
class NilaiListView(BaseListView):
    model = Nilai
    title = 'Data Nilai'
    icon = 'bi-clipboard-data'
    columns = ['Siswa', 'Mapel', 'Jenis', 'Nilai', 'Semester', 'Tahun Ajaran']
    create_url_name = 'akademik:nilai_create'
    edit_url_name = 'akademik:nilai_update'
    delete_url_name = 'akademik:nilai_delete'
    row_builder = staticmethod(lambda o: [
        o.siswa.nama, o.mapel.nama_mapel, o.get_jenis_nilai_display(),
        o.nilai, o.get_semester_display(), o.tahun_ajaran
    ])


class NilaiCreateView(BaseCreateView):
    model = Nilai
    title = 'Nilai'
    fields = ['siswa', 'mapel', 'jenis_nilai', 'nilai', 'semester', 'tahun_ajaran']
    success_url = reverse_lazy('akademik:nilai_list')


class NilaiUpdateView(BaseUpdateView):
    model = Nilai
    title = 'Nilai'
    fields = ['siswa', 'mapel', 'jenis_nilai', 'nilai', 'semester', 'tahun_ajaran']
    success_url = reverse_lazy('akademik:nilai_list')


class NilaiDeleteView(BaseDeleteView):
    model = Nilai
    title = 'Nilai'
    success_url = reverse_lazy('akademik:nilai_list')


# ------------------------------------------------------------------
# KEHADIRAN
# ------------------------------------------------------------------
class KehadiranListView(BaseListView):
    model = Kehadiran
    title = 'Data Kehadiran'
    icon = 'bi-calendar-check'
    columns = ['Siswa', 'Tanggal', 'Status', 'Keterangan']
    create_url_name = 'akademik:kehadiran_create'
    edit_url_name = 'akademik:kehadiran_update'
    delete_url_name = 'akademik:kehadiran_delete'
    row_builder = staticmethod(lambda o: [o.siswa.nama, o.tanggal, o.get_status_display(), o.keterangan])


class KehadiranCreateView(BaseCreateView):
    model = Kehadiran
    title = 'Kehadiran'
    fields = ['siswa', 'tanggal', 'status', 'keterangan']
    success_url = reverse_lazy('akademik:kehadiran_list')


class KehadiranUpdateView(BaseUpdateView):
    model = Kehadiran
    title = 'Kehadiran'
    fields = ['siswa', 'tanggal', 'status', 'keterangan']
    success_url = reverse_lazy('akademik:kehadiran_list')


class KehadiranDeleteView(BaseDeleteView):
    model = Kehadiran
    title = 'Kehadiran'
    success_url = reverse_lazy('akademik:kehadiran_list')


# ------------------------------------------------------------------
# PRESTASI
# ------------------------------------------------------------------
class PrestasiListView(BaseListView):
    model = Prestasi
    title = 'Data Prestasi'
    icon = 'bi-trophy'
    columns = ['Siswa', 'Nama Prestasi', 'Tingkat', 'Tahun']
    create_url_name = 'akademik:prestasi_create'
    edit_url_name = 'akademik:prestasi_update'
    delete_url_name = 'akademik:prestasi_delete'
    row_builder = staticmethod(lambda o: [o.siswa.nama, o.nama_prestasi, o.get_tingkat_display(), o.tahun])


class PrestasiCreateView(BaseCreateView):
    model = Prestasi
    title = 'Prestasi'
    fields = ['siswa', 'nama_prestasi', 'tingkat', 'tahun', 'keterangan']
    success_url = reverse_lazy('akademik:prestasi_list')


class PrestasiUpdateView(BaseUpdateView):
    model = Prestasi
    title = 'Prestasi'
    fields = ['siswa', 'nama_prestasi', 'tingkat', 'tahun', 'keterangan']
    success_url = reverse_lazy('akademik:prestasi_list')


class PrestasiDeleteView(BaseDeleteView):
    model = Prestasi
    title = 'Prestasi'
    success_url = reverse_lazy('akademik:prestasi_list')
