from rest_framework import serializers
from .models import Guru, Kelas, Siswa, MataPelajaran, Nilai, Kehadiran, Prestasi


class GuruSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guru
        fields = '__all__'


class KelasSerializer(serializers.ModelSerializer):
    wali_kelas_nama = serializers.CharField(source='wali_kelas.nama', read_only=True, default='')

    class Meta:
        model = Kelas
        fields = '__all__'


class SiswaSerializer(serializers.ModelSerializer):
    kelas_nama = serializers.CharField(source='kelas.nama_kelas', read_only=True, default='')
    tingkat = serializers.IntegerField(source='kelas.tingkat', read_only=True, default=None)

    class Meta:
        model = Siswa
        fields = '__all__'


class MataPelajaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataPelajaran
        fields = '__all__'


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
