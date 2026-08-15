from django.contrib import admin
from .models import Siswa


@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nis', 'nisn', 'kelas', 'jenis_kelamin', 'status')
    list_filter = ('kelas', 'jenis_kelamin', 'status')
    search_fields = ('nama', 'nis', 'nisn')
