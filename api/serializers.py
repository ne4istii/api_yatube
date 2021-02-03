from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Post, Comment, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', 
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=200,
        validators=[
            UniqueValidator(
                queryset=Group.objects.all(),
                message='Такая группа уже существует!'
            ),            
        ]
    )

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    post = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,   
    )
    
    class Meta:
        model = Comment
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    
    def validate(self, attrs):
        if attrs.get('user') == attrs.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return super().validate(attrs)

    class Meta:
        model = Follow
        fields = ('user', 'following',)
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже существует!'
            ),
        )
