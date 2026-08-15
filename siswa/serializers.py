from rest_framework import serializers
from .models import Siswa


class SiswaSerializer(serializers.ModelSerializer):
    kelas_nama = serializers.CharField(source='kelas.nama_kelas', read_only=True, default='')
    tingkat = serializers.IntegerField(source='kelas.tingkat', read_only=True, default=None)

    class Meta:
        model = Siswa
        fields = '__all__'
