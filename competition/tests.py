from django.test import TestCase

from .models import * 

class ModelTest(TestCase):

    def setUp(self):
        Competition.objects.create(name='essay')
        Event.objects.create(name='opening', competition=Competition.objects.get(pk=1))
        Team.objects.create(name='synthesis')
        Competition.objects.get(pk=1).teams.add(Team.objects.get(pk=1))
        User.objects.create(name='alex', team=Team.objects.first()) # Auto Presence

    def test_auto_presence_new_user(self):
        self.assertEqual(len(Presence.objects.all()), 1)
    
    def test_presence_new_team(self):
        Team.objects.create(name="team 2")
        User.objects.create(name="user 2", team=Team.objects.get(pk=2))
        Competition.objects.get(pk=1).teams.add(Team.objects.get(pk=2))
        self.assertEqual(len(Presence.objects.all()), 2)

    def test_presence_new_event(self):
        Event.objects.create(name='presentation', competition=Competition.objects.get(pk=1))
        self.assertEqual(len(Presence.objects.all()), 2)

    def test_competition_name_unique(self):
        def create_competition():
            competition1 = Competition(name='essay')
            competition1.save() # Error unique
        self.assertRaises(Exception, create_competition)

    def test_event_name_not_unique(self):
        event1 = Event(name='opening', competition=Competition.objects.get(pk=1))
        event1.save()

    def test_team_name_not_unique(self):
        team1 = Team(name='synthesis')
        team1.save()

    def test_user_name_not_unique(self):
        user1 = User(name='alex', team=Team.objects.first())
        user1.save()

    def test_attend_success(self):
        self.assertEqual(attend(1, 1), 'success')
        self.assertEqual(Presence.objects.get(pk=1).attend, True)

    def test_attend_not_included(self):
        Team.objects.create(name='team 2')
        User.objects.create(name='alex', team=Team.objects.get(pk=2))
        self.assertEqual(attend(2, 1), 'not_included')
        competition = Competition.objects.get(name="Global Event")
        self.assertEqual(len(competition.event_set.all()), 1)
        self.assertEqual(competition.event_set.first().name, "NOT INCLUDED opening")
        self.assertIn(
            User.objects.get(pk=2),
            [presence.user for presence in Presence.objects.filter(event=Event.objects.get(pk=2)).all()]
        )

    def test_add_and_remove_team_on_competition(self):
        Team.objects.create(name='team 2')
        team = Team.objects.get(pk=2)
        User.objects.create(name='user 2', team=team)
        competition = Competition.objects.get(pk=1)

        competition.teams.add(team)
        self.assertEqual(len(Presence.objects.all()), 2)

        competition.teams.remove(team)
        self.assertEqual(len(Presence.objects.all()), 1)

    def test_get_competition(self):
        self.assertEqual(
            get_competition(),
            [{
                'competition_id'    : 1,
                'name'              : 'essay',
                'teams'             : 1,
            }]
        )

    def test_get_event(self):
        self.assertEqual(
            get_event(competition_id=1),
            [{
                'event_id'      : 1,
                'name'          : 'opening',
                'date'          : None,
            }]
        )

    def test_get_event_participant(self):
        self.assertEqual(
            get_event_presence(event_id=1),
            [{
            'user_id'   : 1,
            'name'      : 'alex',
            'team'      : 'synthesis',
            'attend'    : False,
            'datetime'  : None,
            }]
        )
