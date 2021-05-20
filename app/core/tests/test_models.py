from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        '''test creating a  new user with an email is successful'''
        email = 'test@londondev.com'
        password = 'manu2021'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test the email for new user is normailzed'''
        email = 'test@LONDONDEV.COM'
        user = get_user_model().objects.create_user(
            email, 'manu123'
        )
        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        '''Test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'manu123')


    def test_create_new_superuser(self):
        '''test creating a new superuser'''
        user = get_user_model().objects.create_superuser(
            'test@londondev.com',
            'manu123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)