from django.db import models
from tournaments.models import Tournament

class Round(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    ]
    id = models.AutoField(primary_key=True)
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.CASCADE, db_column='tournament_id')
    number = models.IntegerField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')

    class Meta:
        managed = False
        db_table = 'Round'

    def __str__(self):
        return f"Round {self.number} of Tournament {self.tournament.id}"
