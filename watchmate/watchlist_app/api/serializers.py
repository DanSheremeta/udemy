from rest_framework import serializers

from ..models import StreamPlatform, WatchList, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ('watchlist',)


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')

    class Meta:
        model = WatchList
        fields = "__all__"

    def create(self, validated_data):
        validated_data['platform'] = StreamPlatform.objects.get(name=validated_data['platform']['name'])
        return WatchList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['platform'] = StreamPlatform.objects.get(name=validated_data['platform']['name'])
        instance = super(WatchListSerializer, self).update(instance, validated_data)
        return instance


class StreamPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamPlatform
        fields = "__all__"
