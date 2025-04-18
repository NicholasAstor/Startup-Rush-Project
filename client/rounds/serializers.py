from rest_framework import serializers
from .models import Round

class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ['id', 'tournament', 'number', 'status']
