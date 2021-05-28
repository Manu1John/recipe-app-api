from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('user:ingredient-list')

class PublicIngredientApiTests(TestCase):
    '''Test the publicly availabe ingredients api'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''Test that login is required to access the endpoint'''
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTests(TestCase):
    '''Test the privetly availabe ingredient api'''

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            'test@londondev.com',
            'manu123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        '''Test retrieving a list of ingredients'''
        Ingredient.objects.create(user=self.user, name='kale')
        Ingredient.objects.create(user=self.user, name='salt')
        
        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        '''Test that ingredients for the authenticated user are returned'''
        user2 = get_user_model().objects.create_user(
            'other@londondevapp.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='vinager')
        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

