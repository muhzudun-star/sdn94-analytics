from rest_framework import serializers
from .models import Nilai, Kehadiran, Prestasi


class NilaiSerializer(serializers.ModelSerializer):
    siswa_nama = serializers.CharField(source='siswa.nama', read_only=True, default='')
    kelas_nama = serializers.CharField(source='siswa.kelas.nama_kelas', read_only=True, default='')
    mapel_nama = serializers.CharField(source='mapel.nama_mapel', read_only=True, default='')
    kkm = serializers.IntegerField(source='mapel.kkm', read_only=True, default=70)

    class Meta:
        model = Nilai
        fields = '__all__'


class KehadiranSerializer(serializers.ModelSerializer):
    siswa_nama = serializers.CharField(source='siswa.nama', read_only=True, default='')
    kelas_nama = serializers.CharField(source='siswa.kelas.nama_kelas', read_only=True, default='')

    class Meta:
        model = Kehadiran
        fields = '__all__'


class PrestasiSerializer(serializers.ModelSerializer):
    siswa_nama = serializers.CharField(source='siswa.nama', read_only=True, default='')
    kelas_nama = serializers.CharField(source='siswa.kelas.nama_kelas', read_only=True, default='')

    class Meta:
        model = Prestasi
        fields = '__all__'
