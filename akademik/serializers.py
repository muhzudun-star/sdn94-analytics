from rest_framework import serializers
from .models import Kelas, MataPelajaran


class KelasSerializer(serializers.ModelSerializer):
    wali_kelas_nama = serializers.CharField(source='wali_kelas.nama', read_only=True, default='')

    class Meta:
        model = Kelas
        fields = '__all__'


class MataPelajaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = MataPelajaran
        fields = '__all__'
