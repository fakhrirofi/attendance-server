from django.db import models

class Team(models.Model):
    name = models.CharField("team name", max_length=20, unique=True)

    def __str__(self) -> str:
        return f"<Team {self.name}>"

class User(models.Model):
    name = models.CharField("name", max_length=30, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"<User {self.name}>"

class Event(models.Model):
    name = models.CharField("event name", max_length=30)

    def __str__(self) -> str:
        return f"<Event {self.name}>"

class Presence(models.Model):
    user = models.ManyToManyField(User)
    event = models.ManyToManyField(Event)
    date = models.DateTimeField('date')

    def __str__(self) -> str:
        return f"<Presence {self.user.name} on {self.event.name}>"

