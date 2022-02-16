from rest_framework import exceptions, mixins, viewsets, serializers
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Article
from .permissions import IsAuthor
from .serializers import ArticleSerializer, RegisterSerializer

User = get_user_model()


class RegisterViewSet(viewsets.GenericViewSet, 
                mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ArticleViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin):
    authentication_classes = [BasicAuthentication]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthor]
    
    def list(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous and (self.request.user.is_subscriber or self.request.user.is_author):
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(is_public=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if (not instance.is_public) and not (self.request.user.is_subscriber or self.request.user.is_author):
             raise exceptions.PermissionDenied()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
