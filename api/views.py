from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from .filters import PostFilter, FollowFilter
from .models import Post, Group
from .permissions import IsResourceOwner
from .serializers import (
    CommentSerializer, PostSerializer, 
    GroupSerializer, FollowSerializer
)


User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsResourceOwner)
    

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsResourceOwner)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsResourceOwner)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        queryset = post.comments.all()
        return queryset
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, IsResourceOwner)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FollowFilter

    def get_queryset(self):
        author = get_object_or_404(User, username=self.request.user)
        queryset = author.following.all()
        return queryset
