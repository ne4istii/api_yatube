from rest_framework import serializers


class FollowUserValidator:

    def __call__(self, data):
        if data.get('user') == data.get('following'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
