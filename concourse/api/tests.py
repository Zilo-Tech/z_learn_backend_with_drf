from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from concourse.models import Concourse, ConcourseRegistration, ConcoursePastPapers

class ConcoursePastPaperDetailViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.concourse = Concourse.objects.create(concourseName='Test Concourse', concourseSubName='Sub Test', price=100)
        self.registration = ConcourseRegistration.objects.create(user=self.user, concourse=self.concourse, payment_status=True, phoneNumber='1234567890')
        self.past_paper = ConcoursePastPapers.objects.create(concourse=self.concourse, subject='Math', file='path/to/file', year=2021)
        self.url = reverse('concourse-past-paper-detail', kwargs={'concourse_id': self.concourse.id, 'paper_id': self.past_paper.id})

    def test_access_past_paper_with_payment(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], 'Math')

    def test_access_past_paper_without_payment(self):
        self.registration.payment_status = False
        self.registration.save()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_past_paper_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ConcourseTotalUsersEnrolledTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword')
        self.concourse = Concourse.objects.create(concourseName='Test Concourse', concourseSubName='Sub Test', price=100)
        self.registration = ConcourseRegistration.objects.create(user=self.user, concourse=self.concourse, payment_status=True, phoneNumber='1234567890')
        self.url = reverse('total_users_enroll_for_concourse', kwargs={'concourse_id': self.concourse.id})

    def test_total_users_enrolled(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_users_enrolled'], 1)

    def test_total_users_enrolled_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)