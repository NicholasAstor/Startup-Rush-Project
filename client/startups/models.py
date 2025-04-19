from django.db import models

class Startup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=255)
    year_foundation = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'Startup'

    def __str__(self):
        return "Startup name: "+ self.name

class StartupStatistics(models.Model):
    startup = models.OneToOneField('Startup', on_delete=models.CASCADE, primary_key=True, db_column='startup_id')
    total_pitches = models.IntegerField(default=0, null=True, blank=True)
    total_bugs = models.IntegerField(default=0, null=True, blank=True)
    total_traction = models.IntegerField(default=0, null=True, blank=True)
    total_pissed_investors = models.IntegerField(default=0, null=True, blank=True)
    total_fakenews = models.IntegerField(default=0, null=True, blank=True)
    total_sharkfights = models.IntegerField(default=0, null=True, blank=True)
    total_wins = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Startup_Statistics'

    def __str__(self):
        return f"Statistics for {self.startup.name}"