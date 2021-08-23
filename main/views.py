from django.db.models import Q
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from main.models import *
from main.permissions import IsAuthorPermission
from main.serializers import *


class PaginationView(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = []
        return [permission() for permission in permissions]


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = PaginationView
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ['GET', 'POST', 'PUT', 'DELETE']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def post(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        post = Post.objects.create(user=request.user, **validated_data)
        for image in images_data.getlist('images'):
            Images.objects.create(image=image, post=post)
        return post

    def get_permissions(self):
        if self.action in ['update', 'partial-update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def own(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsView(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    pagination_class = PaginationView
    permission_classes = [IsAuthenticated]

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['action'] = self.action
    #     return context


class LikesView(ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['action'] = self.action
    #     return context


class RatingView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_ratings(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)
        serializers = RatingSerializer(queryset, many=True, context={'request': request})
        return Response(serializers.data, 200)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class BookmarkView(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def bookmarks(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)
        serializer = BookmarkSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}
