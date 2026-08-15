from django.contrib import admin
from .models import Nilai, Kehadiran, Prestasi


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
