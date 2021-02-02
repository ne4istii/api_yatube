from django_filters import rest_framework as filters

from .models import Post, Follow


class PostFilter(filters.FilterSet):

    class Meta:
        model = Post
        fields = ['group']


class FollowFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='user__username')
    
    class Meta:
        model = Follow
        fields = ['search']
