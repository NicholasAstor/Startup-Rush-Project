from rest_framework import serializers
from .models import Battle, EventBattle

class BattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ['id', 'round', 'status', 'startup1', 'startup2', 'winner']

class EventBattleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBattle
        fields = ['id', 'battle', 'event', 'startup']