from rest_framework import viewsets, filters
from .models import Guru
from .serializers import GuruSerializer


class GuruViewSet(viewsets.ModelViewSet):
    queryset = Guru.objects.all()
    serializer_class = GuruSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'nip']
