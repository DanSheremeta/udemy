from rest_framework import serializers

from ..models import StreamPlatform, WatchList


class WatchListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ('id', 'name', 'description', 'activate')
        # exclude = ('id')


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"

    # def get_len_name(self, obj):
    #     return len(obj.name)
    #
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and Description should be different")
    #     else:
    #         return data
    #
    # def validate_name(self, value):
    #     if len(value) < 3:
    #         raise serializers.ValidationError('Name cannot be more than 3 characters')
    #     else:
    #         return value


# def name_len(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Name cannot be more than 2 characters')
#
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_len])
#     description = serializers.CharField()
#     activate = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.activate = validated_data.get('activate', instance.activate)
#         instance.save()
#         return instance
#
#     def validate(self, data):
#
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description should be different")
#         else:
#             return data
#
#     def validate_name(self, value):
#
#         if len(value) < 3:
#             raise serializers.ValidationError('Name cannot be more than 3 characters')
#         else:
#             return value
