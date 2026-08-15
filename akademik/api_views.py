from rest_framework import viewsets, filters
from .models import Kelas, MataPelajaran
from .serializers import KelasSerializer, MataPelajaranSerializer


class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.select_related('wali_kelas').all()
    serializer_class = KelasSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama_kelas']


class MataPelajaranViewSet(viewsets.ModelViewSet):
    queryset = MataPelajaran.objects.all()
    serializer_class = MataPelajaranSerializer
