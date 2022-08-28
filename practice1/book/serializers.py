from rest_framework import serializers

from author.models import Author
from .models import *


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    genre = serializers.CharField()
    language = serializers.CharField()
    author = serializers.CharField()
    description = serializers.CharField()
    date_of_publication = serializers.DateField()
    date_of_writing = serializers.DateField()

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.language = validated_data.get('language', instance.language)
        instance.author = validated_data.get('author', instance.author)
        instance.description = validated_data.get('description', instance.description)
        instance.date_of_publication = validated_data.get('date_of_publication', instance.date_of_publication)
        instance.date_of_writing = validated_data.get('date_of_writing', instance.date_of_writing)
        instance.save()
        return instance
