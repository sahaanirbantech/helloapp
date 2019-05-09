import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Hello
from ..serializers import HelloSerializer

client = Client()

class GetUsernameDOBTest(TestCase):
    def setUp(self):
        self.asaha = Hello.objects.create(
            username='asaha', date_of_birth='1988-04-10')
        self.ankitac = Hello.objects.create(
            username='ankitac', date_of_birth='1988-02-08')

    def test_get_valid_username_dob(self):
        response = client.get(reverse('get_put_username', kwargs={'uname': self.asaha.username}))
        user = Hello.objects.get(username=self.asaha.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_username_dob(self):
        response = client.get(reverse('get_put_username', kwargs={'uname': 'absentUser'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class InsertNewUsernameDOBTest(TestCase):
    def setUp(self):
        self.asaha = Hello.objects.create(
            username='asaha', date_of_birth='1988-04-10')
        self.valid_payload = {
            'dateOfBirth': '1988-04-10'
        }
        self.invalid_payload = {
            'dateOfBirth': '2025-02-03'
        }

    def test_insert_valid_username_dob(self):
        response = client.put(
            reverse('get_put_username', kwargs={'uname': self.asaha.username}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_insert_invalid_username_dob(self):
        response = client.put(
            reverse('get_put_username', kwargs={'uname': self.asaha.username}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
