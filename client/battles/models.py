from django.db import models
from startups.models import Startup
from tournaments.models import Round

class Battle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    id = models.AutoField(primary_key=True)
    round = models.ForeignKey('tournaments.Round', on_delete=models.CASCADE, db_column='round_id')
    startup1 = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, db_column='startup1_id', related_name='startup1')#o nome relativo permite a pesquisa reversa da Startup para a Batalha
    startup2 = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, db_column='startup2_id', related_name='startup2', null=True, blank=True)
    winner = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, null=True, blank=True, db_column='winner_id')
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='pending')
    shark_fight = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Battle'

    def __str__(self):
        return f"Battle {self.id} in Round {self.round.id}"
    
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status, '')
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    impact_score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Event'

    def __str__(self):
        return self.name
    
class EventBattle(models.Model):
    id = models.AutoField(primary_key=True)
    battle = models.ForeignKey('Battle', on_delete=models.CASCADE, db_column='battle_id')
    startup = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, db_column='startup_id')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, db_column='event_id')

    class Meta:
        managed = False
        db_table = 'Event_battle'

    def __str__(self):
        return f"EventBattle {self.id}"


