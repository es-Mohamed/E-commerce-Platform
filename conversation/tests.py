# puddle/conversation/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from items.models import Item, Category # Import Category if needed for Item creation
from .models import Conversation, ConversationMessage

class ConversationModelTest(TestCase):
    """
    Tests for the Conversation models.
    """
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.category = Category.objects.create(name='Test Category') # Ensure category exists
        self.item = Item.objects.create(
            category=self.category,
            name='Sample Item',
            description='Description',
            price=100.00,
            image='image.jpg',
            created_by=self.user1
        )
        # Manually create a conversation for testing purposes
        self.conversation = Conversation.objects.create(item=self.item)
        self.conversation.members.add(self.user1, self.user2)

    def test_conversation_creation(self):
        """
        Verify that a Conversation object is created correctly.
        """
        self.assertTrue(isinstance(self.conversation, Conversation))
        self.assertEqual(self.conversation.item, self.item)
        self.assertIn(self.user1, self.conversation.members.all())
        self.assertIn(self.user2, self.conversation.members.all())
        self.assertIsNotNone(self.conversation.created_at)
        self.assertIsNotNone(self.conversation.modified_at)

    def test_conversation_message_creation(self):
        """
        Verify that a ConversationMessage object is created correctly.
        """
        message = ConversationMessage.objects.create(
            conversation=self.conversation,
            content='Hello, is this available?',
            created_by=self.user2
        )
        self.assertTrue(isinstance(message, ConversationMessage))
        self.assertEqual(message.conversation, self.conversation)
        self.assertEqual(message.content, 'Hello, is this available?')
        self.assertEqual(message.created_by, self.user2)
        self.assertIsNotNone(message.created_at)