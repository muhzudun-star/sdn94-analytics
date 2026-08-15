from django.contrib import admin
from .models import Kelas, MataPelajaran


@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas', 'tingkat', 'tahun_ajaran', 'wali_kelas')
    list_filter = ('tingkat', 'tahun_ajaran')


@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('kode_mapel', 'nama_mapel', 'kkm')
