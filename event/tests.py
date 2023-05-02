from django.test import TestCase
from datetime import timedelta, datetime
from django.urls import reverse
from django.conf import settings
from .user_qr_code import encrypt

from .models import *


class DatabaseTest(TestCase):

    def setUp(self):
        Event.objects.create(
            name='opening',
            datetime=datetime(2023, 4, 24),
            description="blabla",
            group_link="http",
            place="upn",
            is_free=True,
            is_open=True,
            max_participant=2,
        )
        Presence.objects.create(
            name='alex',
            event=Event.objects.first(),
            institution="upn",
            email="alex@student.upnyk.ac.id",
            phone_number = "+628123456789",
            payment_check=False
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
                    'is_free'           : True,
                    'is_open'           : True,
                    'name'              : 'opening',
                    'datetime'          : datetime(2023, 4, 24),
                    'registered'        : 1,
                    'max_participant'   : 2
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
                    'institution'           : 'upn',
                    'email'                 : "alex@student.upnyk.ac.id",
                    'attendance'            : False,
                    'datetime'              : None,
                    'payment_check'         : False
                }
            ]
        )


settings.ENCRYPTION_KEY = 'uKkxAih2i4k81ZGxrsTIHX8hsPt_E4b8XI642sr6sq0='
class APITest(TestCase):
    ENC = encrypt("1")

    def setUp(self):
        Event.objects.create(
            name='opening',
            datetime=datetime(2023, 4, 24),
            description="blabla",
            group_link="http",
            place="upn",
            is_free=True,
            is_open=True,
            max_participant=2,
        )
        Presence.objects.create(
            name='alex',
            event=Event.objects.first(),
            institution="upn",
            email="alex@student.upnyk.ac.id",
            phone_number = "+628123456789",
            payment_check=True
        )

    def test_attend_success(self):
        data = {
            'API_KEY'   : settings.API_KEY,
            'enc'       : self.ENC,
            'event_id'  : 1
        }
        response = self.client.post(
            reverse('api', args=['attend']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data['message'], "ok")
    
    def test_attend_presence_id_not_found(self):
        data = {
            'API_KEY'   : settings.API_KEY,
            'enc'       : encrypt("5"),
            'event_id'  : 1
        }
        response = self.client.post(
            reverse('api', args=['attend']),
            data
        )
        self.assertEqual(response.status_code, 404)

    def test_api_key_not_valid(self):
        data = {
            'API_KEY'   : "haha",
            'enc'       : self.ENC,
            'event_id'  : 1
        }
        response = self.client.post(
            reverse('api', args=['attend']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_data['message'], "authentication error")

    def test_attend_qrcode_not_valid(self):
        data = {
            'API_KEY'   : settings.API_KEY,
            'enc'       : "haha",
            'event_id'  : 1
        }
        response = self.client.post(
            reverse('api', args=['attend']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['message'], "qr_code")
        
    def test_attend_different_event(self):
        data = {
            'API_KEY'   : settings.API_KEY,
            'enc'       : self.ENC,
            'event_id'  : 2
        }
        response = self.client.post(
            reverse('api', args=['attend']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['message'], "different_event")

    def test_attend_payment_not_check(self):
        presence = Presence.objects.get(pk=1)
        presence.payment_check = False
        presence.save()
        data = {
            'API_KEY'   : settings.API_KEY,
            'enc'       : self.ENC,
            'event_id'  : 1
        }
        response = self.client.post(
            reverse('api', args=['attend']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data['message'], "payment_check")

    def test_get_events(self):
        data = {
            'API_KEY'   : settings.API_KEY,
        }
        response = self.client.post(
            reverse('api', args=['get_events']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data,
            [
                {
                    'id'                : 1,
                    'is_free'           : True,
                    'is_open'           : True,
                    'name'              : 'opening',
                    'datetime'          : '2023-04-24T00:00:00',
                    'registered'        : 1,
                    'max_participant'   : 2
                }
            ] 
        )

    def test_get_event_presence(self):
        data = {
            'API_KEY'   : settings.API_KEY,
            'event_id'  : 1
        }
        response = self.client.post(
            reverse('api', args=['get_event_presence']),
            data
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data,
            [
                {
                    'name'                  : 'alex',
                    'institution'           : 'upn',
                    'email'                 : "alex@student.upnyk.ac.id",
                    'attendance'            : False,
                    'datetime'              : None,
                    'payment_check'         : True
                }
            ]
        )

    def test_get_event_presence_event_id_not_found(self):
        data = {
            'API_KEY'   : settings.API_KEY,
            'event_id'  : 3
        }
        response = self.client.post(
            reverse('api', args=['get_event_presence']),
            data
        )
        self.assertEqual(response.status_code, 404)