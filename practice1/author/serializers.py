from rest_framework import serializers

from .models import *


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    surname = serializers.CharField()
    birth_date = serializers.DateField()
    age = serializers.IntegerField()
    death_date = serializers.DateField()

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.age = validated_data.get('age', instance.age)
        instance.death_date = validated_data.get('death_date', instance.death_date)
        instance.save()
        return instance
