from rest_framework import serializers
from core.models import Tag,Ingredient

class TagSerializers(serializers.ModelSerializer):
    '''serializer for the object'''

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    '''serializers for ingredient objects'''
    
    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_fields = ('id',)