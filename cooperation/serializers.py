import datetime

from rest_framework import serializers
from .models import Cooperation, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'firstname', 'lastname', 'room_number')


class CooperationReadSerializer(serializers.ModelSerializer):
    creator = CustomUserSerializer(read_only=True)
    participants = CustomUserSerializer(many=True, required=False)

    class Meta:
        model = Cooperation
        fields = ('id', 'title', 'description', 'date', 'creator', 'participants')


class CooperationWriteSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)
    creator = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Cooperation
        fields = ('id', 'title', 'description', 'date', 'creator', 'participants')

    def validate_creator(self, value):
        if Cooperation.objects.filter(creator_id=value).exists():
            raise serializers.ValidationError(f"User with id: {value.id} already have cooperation!")
        return value

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Short title")
        return value

    # def validate_date(self, date):
    #     delta = date.replace(tzinfo=None)-datetime.datetime.now()
    #     if delta >= datetime.timedelta(minutes=30):
    #         return date
    #     return serializers.ValidationError('Создать совместное приготовление можно не меньше чем за 30 минут')
