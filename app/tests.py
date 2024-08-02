from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Poll, Question, User

# Write your test cases here.

class PollAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", 
            first_name="Test", 
            last_name="User", 
            password="password123"
        )
        self.poll = Poll.objects.create(title="Test Poll", creater=self.user)
        self.question = Question.objects.create(
            title="Test Question", 
            choices="Choice 1, Choice 2"
        )
        self.poll.questions.add(self.question)
        self.poll.save()

    def test_create_poll(self):
        url = reverse('create-list-poll')
        data = {
            'title': 'New Poll',
            'creater': 'testuser@example.com',
            'questions': [
                {'title': 'New Question', 'choices': 'Option 1, Option 2'}
            ],
            'is_open': True
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Poll')
        self.assertEqual(response.data['creater'], 'testuser@example.com')

    def test_get_polls(self):
        url = reverse('create-list-poll')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Test Poll")

    def test_update_poll(self):
        url = reverse('update-poll', kwargs={'id': self.poll.id})
        data = {
            'title': 'Updated Poll',
            'creater': 'testuser@example.com',
            'questions': [
                {'title': 'Updated Question', 'choices': 'Option 1, Option 2'}
            ],
            'is_open': False
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Poll')
        self.assertNotIn('creater', response.data)
        self.assertEqual(response.data['is_open'], False)

    def test_partial_update_poll(self):
        url = reverse('update-poll', kwargs={'id': self.poll.id})
        data = {
            "is_open": False
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_open'], False)

    def test_delete_poll(self):
        url = reverse('delete-poll', kwargs={'id': self.poll.id})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Poll.objects.filter(id=self.poll.id).exists())
