from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Poll, Question, User

# Write your test cases here.

class PollAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", first_name="Test", last_name="User", password="password123")
        self.poll = Poll.objects.create(title="Test Poll", creater=self.user)
        self.question = Question.objects.create(title="Test Question", choices="Choice 1, Choice 2")
        self.poll.questions.add(self.question)
        self.poll.save()

    def test_create_poll(self):
        url = reverse('poll-create')
        data = {
            "title": "New Poll",
            "creater": self.user.id,
            "questions": [self.question.id],
            "is_open": True
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Your Data has been Saved Successfully")

    def test_get_polls(self):
        url = reverse('poll-create')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['title'], "Test Poll")

    def test_update_poll(self):
        url = reverse('poll-detail', kwargs={'id': self.poll.id})
        data = {
            "id": self.poll.id,
            "title": "Updated Poll",
            "creater": self.user.id,
            "questions": [self.question.id],
            "is_open": False
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Your data has been updated successfully.")
        self.assertEqual(response.data['payload']['title'], "Updated Poll")

    def test_partial_update_poll(self):
        url = reverse('poll-detail', kwargs={'id': self.poll.id})
        data = {
            "id": self.poll.id,
            "is_open": False
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Your data has been updated successfully.")
        self.assertEqual(response.data['payload']['is_open'], False)

    def test_delete_poll(self):
        url = reverse('poll-detail', kwargs={'id': self.poll.id})
        data = {
            "id": self.poll.id
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Record has been Deleted Successfully!")
        self.assertFalse(Poll.objects.filter(id=self.poll.id).exists())
