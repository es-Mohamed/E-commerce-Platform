# puddle/core/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from items.models import Category, Item
from django.contrib.auth.models import User
from django.utils import translation

class CoreViewsTest(TestCase):
    """
    Tests for views in the Core application.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Books')
        self.item = Item.objects.create(
            category=self.category,
            name='Test Book',
            description='A test book',
            price=25.00,
            image='path/to/image.jpg',
            created_by=self.user
        )
        # Initialize translations
        with translation.override('ar'):
            self.item.name = 'كتاب اختبار'
            self.item.description = 'كتاب للاختبار'
            self.item.save()
            self.category.name = 'كتب'
            self.category.save()

    def test_index_view_status_code(self):
        """
        Verify that the index view returns a 200 OK status code.
        """
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        """
        Verify that the index view uses the correct template.
        """
        response = self.client.get(reverse('core:index'))
        self.assertTemplateUsed(response, 'core/index.html')

    def test_index_view_context_data(self):
        """
        Verify that the index view passes the correct context data to the template.
        """
        response = self.client.get(reverse('core:index'))
        self.assertIn('items', response.context)
        self.assertIn('categories', response.context)
        self.assertEqual(len(response.context['items']), 1) # We have one item
        self.assertEqual(len(response.context['categories']), 1) # We have one category

    def test_index_view_content_translation(self):
        """
        Verify that the content in the index view translates correctly.
        """
        # Test with English language
        response = self.client.get(reverse('core:index'), HTTP_ACCEPT_LANGUAGE='en')
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Books')

        # Test with Arabic language
        response = self.client.get(reverse('core:index'), HTTP_ACCEPT_LANGUAGE='ar')
        self.assertContains(response, 'كتاب اختبار')
        self.assertContains(response, 'كتب')