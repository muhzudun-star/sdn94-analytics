from django.urls import reverse_lazy

from common.mixins import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Guru


# ------------------------------------------------------------------
# GURU
# ------------------------------------------------------------------
class GuruListView(BaseListView):
    model = Guru
    title = 'Data Guru'
    icon = 'bi-person-badge'
    columns = ['NIP', 'Nama', 'Jenis Kelamin', 'No. HP', 'Alamat']
    create_url_name = 'kepegawaian:guru_create'
    edit_url_name = 'kepegawaian:guru_update'
    delete_url_name = 'kepegawaian:guru_delete'
    row_builder = staticmethod(lambda o: [o.nip, o.nama, o.get_jenis_kelamin_display(), o.no_hp, o.alamat])


class GuruCreateView(BaseCreateView):
    model = Guru
    title = 'Guru'
    fields = ['nip', 'nama', 'jenis_kelamin', 'no_hp', 'alamat', 'tanggal_bergabung']
    success_url = reverse_lazy('kepegawaian:guru_list')


class GuruUpdateView(BaseUpdateView):
    model = Guru
    title = 'Guru'
    fields = ['nip', 'nama', 'jenis_kelamin', 'no_hp', 'alamat', 'tanggal_bergabung']
    success_url = reverse_lazy('kepegawaian:guru_list')


class GuruDeleteView(BaseDeleteView):
    model = Guru
    title = 'Guru'
    success_url = reverse_lazy('kepegawaian:guru_list')
