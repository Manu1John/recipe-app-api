from core.models import Tag
from  .serializers import TagSerializers
from rest_framework import viewsets,mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    '''Manage tags in the database'''
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)
    seralizer_class = TagSerializers
    queryset = Tag.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user).order_by('-name')