from rest_framework import viewsets, filters
from .models import Guru, Kelas, Siswa, MataPelajaran, Nilai, Kehadiran, Prestasi
from .serializers import (
    GuruSerializer, KelasSerializer, SiswaSerializer, MataPelajaranSerializer,
    NilaiSerializer, KehadiranSerializer, PrestasiSerializer,
)


class GuruViewSet(viewsets.ModelViewSet):
    queryset = Guru.objects.all()
    serializer_class = GuruSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'nip']


class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.select_related('wali_kelas').all()
    serializer_class = KelasSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama_kelas']


class SiswaViewSet(viewsets.ModelViewSet):
    queryset = Siswa.objects.select_related('kelas').all()
    serializer_class = SiswaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'nis', 'nisn']

    def get_queryset(self):
        qs = super().get_queryset()
        kelas_id = self.request.query_params.get('kelas')
        if kelas_id:
            qs = qs.filter(kelas_id=kelas_id)
        return qs


class MataPelajaranViewSet(viewsets.ModelViewSet):
    queryset = MataPelajaran.objects.all()
    serializer_class = MataPelajaranSerializer


class NilaiViewSet(viewsets.ModelViewSet):
    queryset = Nilai.objects.select_related('siswa', 'mapel', 'siswa__kelas').all()
    serializer_class = NilaiSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        mapel_id = self.request.query_params.get('mapel')
        siswa_id = self.request.query_params.get('siswa')
        if mapel_id:
            qs = qs.filter(mapel_id=mapel_id)
        if siswa_id:
            qs = qs.filter(siswa_id=siswa_id)
        return qs


class KehadiranViewSet(viewsets.ModelViewSet):
    queryset = Kehadiran.objects.select_related('siswa', 'siswa__kelas').all()
    serializer_class = KehadiranSerializer


class PrestasiViewSet(viewsets.ModelViewSet):
    queryset = Prestasi.objects.select_related('siswa', 'siswa__kelas').all()
    serializer_class = PrestasiSerializer
