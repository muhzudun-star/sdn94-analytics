from django.contrib import admin
from .models import Guru


@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nip', 'jenis_kelamin', 'no_hp')
    search_fields = ('nama', 'nip')
