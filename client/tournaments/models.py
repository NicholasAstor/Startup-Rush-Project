from django.db import models
from startups.models import Startup

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    ]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ongoing')
    champion = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, null=True, blank=True, db_column='champion_id')
    qty_startups = models.IntegerField()
    qty_rounds = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Tournament'

    def __str__(self):
        return f"Tournament {self.id}"

class StartupTournament(models.Model):
    startup = models.ForeignKey('startups.Startup', on_delete=models.CASCADE, db_column='startup_id')
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, db_column='tournament_id')
    score = models.IntegerField(default=70, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Startup_tournament'

    def __str__(self):
        return f"{self.startup.name} in Tournament {self.tournament.id}"