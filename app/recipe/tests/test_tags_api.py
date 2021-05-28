from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import testcases
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializers



TAGS_URL = ('recipe:tag-list')

class PublicTagsApiTests(testcases):
    '''test the publicly availabe tag Api'''
    def setup(self):
        self.client = APIClient()

    def test_login_required(self):
        '''test the login is required for retrieving tags'''
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTest(testcases):
    '''test the authorized tags api'''
    def setup(self):
        self.user = get_user_model().objects.create_user(
            'test@londondev.com',
            'manu123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_tags(self):
        '''Test retrieving tags'''
        Tag.objects.create(user = self.user, name='vega')
        Tag.objects.create(user = self.user, name ='desert')

        res = self.client.get(TAGS_URL)
        tags =Tag.objects.all().order_by('-name') 
        serializer = TagSerializers(tags, many=True)
        self.asssertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        '''Test that tags returned to authenticate user'''
        user2 = get_user_model().objects.create_user(
            'other@londondevapp.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='comfortfood')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        '''Test creating a new tag'''
        paylod = {'name':'test tag'}
        self.client.post(TAGS_URL,paylod)

        exists = Tag.objects.filter(
            user = self.user,
            name = paylod['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        '''Test creating  a new tag with invalid paylod'''
        paylod = {'name':''}

        res = self.client.post(TAGS_URL, paylod)
            
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)





    


