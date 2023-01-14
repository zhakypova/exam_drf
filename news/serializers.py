from rest_framework import serializers
from .models import *


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['author', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'news']

    def create(self, validated_data):
        news_id = validated_data.pop('news_id')
        validated_data['news_id'] = news_id
        validated_data['author'] = self.context['request'].user.author
        return super().create(validated_data)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ['author', 'news']
