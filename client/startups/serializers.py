from rest_framework import serializers
from .models import *

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = ['id', 'name', 'slogan', 'year_foundation', 'active']

class StartupStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartupStatistics
        fields = ['id', 'startup', 'total_pitches', 'total_bugs', 'total_traction', 'total_pissed_investors', 'total_fakenews', 'total_sharkfights', 'total_wins']

