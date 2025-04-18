from django.db import models

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
