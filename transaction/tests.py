from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Lunch,Users
from users.models import Organization

class LunchDetailViewTestCase(TestCase):
    def setUp(self):
        # Create a test organization
        self.organization = Organization.objects.create(
            name="Test Organization",
            lunch_price=10.00,
            currency="USD"
        )

        # Create a test user
        self.user = Users.objects.create(
            org=self.organization,
            first_name="John",
            last_name="Doe",
            email="johndoe@example.com",
            username="johndoe",
            password="password123",
            lunch_credit_balance=0.00,
            # Other user fields...
        )

        # Create a test lunch entry
        self.lunch = Lunch.objects.create(
            sender_id=self.user,
            reciever_id=self.user,
            quantity=2,
            redeemed=False,
            note="Test lunch"
        )

    def test_get_single_lunch(self):
        # Initialize the test client
        client = APIClient()

        # Get the URL for the lunch detail view, replacing `{lunch_id}` with the actual lunch ID
        url = reverse('lunch-detail', args=[str(self.lunch.pk)])

        # Authenticate the user (if required)
        client.force_authenticate(user=self.user)

        # Send a GET request to retrieve the lunch
        response = client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the expected values
        self.assertEqual(response.data['sender_id'], self.user.id)
        self.assertEqual(response.data['reciever_id'], self.user.id)
        self.assertEqual(response.data['quantity'], self.lunch.quantity)
        self.assertEqual(response.data['redeemed'], self.lunch.redeemed)
        self.assertEqual(response.data['note'], self.lunch.note)

# To test run >> python manage.py test transaction.tests.LunchDetailViewTestCase

