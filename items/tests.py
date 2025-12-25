# puddle/items/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Category, Item
from django.utils import translation

class CategoryModelTest(TestCase):
    """
    Tests for the Category model.
    """
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.category = Category.objects.create(name='Test Category')
        # Set a translation for 'ar'
        with translation.override('ar'):
            self.category.name = 'فئة اختبار'
            self.category.save()

    def test_category_creation(self):
        """
        Verify that a Category object is created correctly.
        """
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_translation(self):
        """
        Verify that category name translation works correctly.
        """
        self.assertEqual(self.category.name_en, 'Test Category')
        self.assertEqual(self.category.name_ar, 'فئة اختبار')

        with translation.override('ar'):
            self.assertEqual(self.category.name, 'فئة اختبار')
        with translation.override('en'):
            self.assertEqual(self.category.name, 'Test Category')


class ItemModelTest(TestCase):
    """
    Tests for the Item model.
    """
    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Electronics')
        self.item = Item.objects.create(
            category=self.category,
            name='Laptop',
            description='A powerful laptop',
            price=1200.00,
            image='path/to/image.jpg', # Must be a valid image path or None if optional
            created_by=self.user
        )
        # Set a translation for 'ar' for the item
        with translation.override('ar'):
            self.item.name = 'لابتوب'
            self.item.description = 'لابتوب قوي'
            self.item.save()

    def test_item_creation(self):
        """
        Verify that an Item object is created correctly.
        """
        self.assertTrue(isinstance(self.item, Item))
        self.assertEqual(self.item.name, 'Laptop')
        self.assertEqual(self.item.price, 1200.00)
        self.assertFalse(self.item.is_sold)
        self.assertEqual(str(self.item), 'Laptop')
        self.assertEqual(self.item.created_by, self.user)
        self.assertEqual(self.item.category, self.category)

    def test_item_translation(self):
        """
        Verify that item name and description translation work correctly.
        """
        self.assertEqual(self.item.name_en, 'Laptop')
        self.assertEqual(self.item.name_ar, 'لابتوب')
        self.assertEqual(self.item.description_en, 'A powerful laptop')
        self.assertEqual(self.item.description_ar, 'لابتوب قوي')

        with translation.override('ar'):
            self.assertEqual(self.item.name, 'لابتوب')
            self.assertEqual(self.item.description, 'لابتوب قوي')
        with translation.override('en'):
            self.assertEqual(self.item.name, 'Laptop')
            self.assertEqual(self.item.description, 'A powerful laptop')