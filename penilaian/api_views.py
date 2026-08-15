from rest_framework import viewsets
from .models import Nilai, Kehadiran, Prestasi
from .serializers import NilaiSerializer, KehadiranSerializer, PrestasiSerializer


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
