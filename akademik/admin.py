from django.contrib import admin
from .models import Guru, Kelas, Siswa, MataPelajaran, Nilai, Kehadiran, Prestasi


@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'jenis_kelamin', 'no_hp')
    search_fields = ('nama', 'nip')


@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ('nama_kelas', 'tingkat', 'tahun_ajaran', 'wali_kelas')
    list_filter = ('tingkat', 'tahun_ajaran')


@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nis', 'nisn', 'kelas', 'jenis_kelamin', 'status')
    list_filter = ('kelas', 'jenis_kelamin', 'status')
    search_fields = ('nama', 'nis', 'nisn')


@admin.register(MataPelajaran)
class MataPelajaranAdmin(admin.ModelAdmin):
    list_display = ('kode_mapel', 'nama_mapel', 'kkm')


@admin.register(Nilai)
class NilaiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'mapel', 'jenis_nilai', 'nilai', 'semester', 'tahun_ajaran')
    list_filter = ('mapel', 'jenis_nilai', 'semester', 'tahun_ajaran')
    search_fields = ('siswa__nama',)


@admin.register(Kehadiran)
class KehadiranAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'tanggal', 'status')
    list_filter = ('status', 'tanggal')
    search_fields = ('siswa__nama',)


@admin.register(Prestasi)
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'nama_prestasi', 'tingkat', 'tahun')
    list_filter = ('tingkat', 'tahun')
    search_fields = ('siswa__nama', 'nama_prestasi')
