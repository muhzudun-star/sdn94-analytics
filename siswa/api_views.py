from rest_framework import viewsets, filters
from .models import Siswa
from .serializers import SiswaSerializer


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
