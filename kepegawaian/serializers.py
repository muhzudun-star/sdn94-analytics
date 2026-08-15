from rest_framework import serializers
from .models import Guru


class GuruSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guru
        fields = '__all__'
