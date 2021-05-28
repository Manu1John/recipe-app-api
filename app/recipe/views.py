from core.models import Tag, Ingredient
from  .serializers import TagSerializers,IngredientSerializer
from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,mixins.CreateModelMixin):
    '''Manage tags in the database'''
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)
    seralizer_class = TagSerializers
    queryset = Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-name')

    
    def perform_create(self, serializer):
        '''create a new tag'''
        serializer.save(user=self.request.user)

class IngredientViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    '''Manage ingredients in the data base'''
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)
    serailizer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        '''Return objects for the curent authentication user'''
        return self.queryset.filter(user=self.request.user).order_by('-name ')