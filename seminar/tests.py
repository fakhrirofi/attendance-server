from django.test import TestCase
from datetime import timedelta, datetime

from .models import *

class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(
            name='opening',
            datetime=datetime(2023, 4, 24),
            max_participant=2
        )
        Presence.objects.create(
            name='alex',
            event=Event.objects.first(),
            institution_origin="upn",
            email="alex@student.upnyk.ac.id",
            phone_number = "+628123456789"
        )
    
    def test_attendance_payment_not_checked(self):
        res = attend(Presence.objects.first().pk)
        self.assertEqual(res, "payment not checked")
    
    def test_attendance_success(self):
        p = Presence.objects.first()
        p.payment_check = True
        p.save()
        res = attend(p.pk)
        self.assertEqual(res, "success")
    
    def test_get_events(self):
        res = get_events()
        self.assertEqual(
            res,
            [
                {
                    'id'                : 1,
                    'name'              : 'opening',
                    'datetime'          : datetime(2023, 4, 24),
                    'registered'        : 1,
                    'max_participant'   : None
                }
            ]
        )

    def test_get_event_presence(self):
        res = get_event_presence(Event.objects.first().pk)
        self.assertEqual(
            res, 
            [
                {
                    'name'                  : 'alex',
                    'institution_origin'    : 'upn',
                    'email'                 : "alex@student.upnyk.ac.id",
                    'attendance'            : False,
                    'datetime'              : None
                }
            ]
        )