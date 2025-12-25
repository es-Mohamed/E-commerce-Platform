# puddle/Dashboard/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from items.models import Category, Item

class DashboardViewsTest(TestCase):
    """
    Tests for views in the Dashboard application.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.category = Category.objects.create(name='Electronics')
        self.item_by_user = Item.objects.create(
            category=self.category,
            name='User Laptop',
            description='Laptop by testuser',
            price=1000.00,
            image='path/to/image1.jpg',
            created_by=self.user
        )
        self.item_by_other_user = Item.objects.create(
            category=self.category,
            name='Other Laptop',
            description='Laptop by otheruser',
            price=1500.00,
            image='path/to/image2.jpg',
            created_by=self.other_user
        )

    def test_index_view_requires_login(self):
        """
        Verify that the dashboard index view redirects to login if not authenticated.
        """
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 302) # Expect redirect to login

    def test_index_view_shows_user_items(self):
        """
        Verify that the dashboard index view shows only items created by the logged-in user.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Dashboard/index.html')
        self.assertIn('items', response.context)
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['items'][0], self.item_by_user)
        self.assertNotContains(response, 'Other Laptop') # Should not contain item from other user

    def test_index_view_does_not_show_other_users_items(self):
        """
        Verify that the dashboard index view does not show items from other users.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard:index'))
        self.assertNotContains(response, self.item_by_other_user.name)