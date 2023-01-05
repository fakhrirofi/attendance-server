from django.test import TestCase

from .models import * 

class ModelTest(TestCase):

    def setUp(self):
        Team.objects.create(name='synthesis')
        User.objects.create(user_id=1, name='alex', team=Team.objects.first())
        Event.objects.create(event_id=1, name='opening')
        event = Event.objects.get(name='opening')
        event.participant.add(Team.objects.get(name='synthesis'))

    def test_team_name_unique(self):
        def create_team():
            team1 = Team(name='synthesis')
            team1.save() # Error unique
        self.assertRaises(Exception, create_team)

    def test_user_must_have_team(self):
        def create_user():
            user1 = User(name='alex')
            user1.save()
        self.assertRaises(Exception, create_user)

    def test_user_name_not_unique(self):
        user1 = User(name='alex', team=Team.objects.first())
        user1.save()

    def test_event_name_unique(self):
        def create_event():
            event1 = Event(name='opening')
            event1.save() # Error unique
        self.assertRaises(Exception, create_event)

    def test_attend_success(self):
        self.assertEqual(attend(1, 1), 'success')

    def test_attend_not_included(self):
        Team.objects.create(name='second')
        User.objects.create(name='alex', team=Team.objects.get(pk=2))
        self.assertEqual(attend(2, 1), 'not_included')
        self.assertEqual(f"NOT INCLUDED opening", Event.objects.get(pk=2).name)
        self.assertIn(
            User.objects.get(pk=2),
            [presence.user for presence in Presence.objects.filter(event=Event.objects.get(pk=2)).all()]
        )
        # another user
        User.objects.create(name='alex', team=Team.objects.get(pk=2))
        self.assertEqual(attend(3, 1), 'not_included')
        self.assertEqual(len(Event.objects.all()), 2)
        self.assertEqual(len(Presence.objects.filter(event=Event.objects.get(pk=2)).all()), 2)

    def test_new_user_team_already_on_event(self):
        User.objects.create(name="alex 2", team=Team.objects.get(pk=1))
        self.assertEqual(len(Presence.objects.all()), 2)

    def test_add_and_remove_team_on_event(self):
        Team.objects.create(name='team 2')
        team = Team.objects.get(pk=2)
        User.objects.create(name='user 2', team=team)
        event = Event.objects.get(event_id=1)

        event.participant.add(team)
        self.assertEqual(len(Presence.objects.all()), 2)

        event.participant.remove(team)
        self.assertEqual(len(Presence.objects.all()), 1)

    def test_get_event(self):
        self.assertEqual(
            get_events(),
            [{
                'event_id'  : 1,
                'name'      : 'opening',
                'date'      : None,
                'team_count': 1
            }]
        )

    def test_get_event_participant(self):
        self.assertEqual(
            get_event_participant(1),
            [{
            'name'      : 'alex',
            'team'      : 'synthesis',
            'attend'    : False,
            'datetime'  : None
            }]
        )
