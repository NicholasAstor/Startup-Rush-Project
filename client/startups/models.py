from django.db import models

class Startup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slogan = models.CharField(max_length=255)
    year_foundation = models.IntegerField()
    score = models.IntegerField(default=70, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'Startup'

    def __str__(self):
        return "Startup name: "+ self.name


class Tournament(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    ]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='ongoing')
    champion = models.ForeignKey('Startup', on_delete=models.CASCADE, null=True, blank=True, db_column='champion_id')

    class Meta:
        managed = False
        db_table = 'Tournament'

    def __str__(self):
        return f"Tournament {self.id}"


class Round(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
    ]
    id = models.AutoField(primary_key=True)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, db_column='tournament_id')
    number = models.IntegerField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')

    class Meta:
        managed = False
        db_table = 'Round'

    def __str__(self):
        return f"Round {self.number} of Tournament {self.tournament.id}"


class Battle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    round = models.ForeignKey('Round', on_delete=models.CASCADE, db_column='round_id')
    startup1 = models.ForeignKey('Startup', on_delete=models.CASCADE, db_column='startup1_id', related_name='startup1')#o nome relativo permite a pesquisa reversa da Startup para a Batalha
    startup2 = models.ForeignKey('Startup', on_delete=models.CASCADE, db_column='startup2_id', related_name='startup2')
    winner = models.ForeignKey('Startup', on_delete=models.CASCADE, null=True, blank=True, db_column='winner_id')
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='pending')
    shark_fight = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Battle'

    def __str__(self):
        return f"Battle {self.id} in Round {self.round.id}"


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)
    impact_score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Event'

    def __str__(self):
        return self.name


class EventBattle(models.Model):
    battle = models.ForeignKey('Battle', on_delete=models.CASCADE, db_column='battle_id')
    startup = models.ForeignKey('Startup', on_delete=models.CASCADE, db_column='startup_id')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, db_column='event_id')

    class Meta:
        managed = False
        db_table = 'EventBattle'

    def __str__(self):
        return f"EventBattle {self.id}"


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
        db_table = 'StartupStatistics'

    def __str__(self):
        return f"Statistics for {self.startup.name}"