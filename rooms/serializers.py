# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer

from .models import Amenity, Room


class AmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = ("name", "description")


class RoomListSerializer(serializers.ModelSerializer):

    average_rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("pk", "name", "country", "city", "price", "average_rating", "is_owner")
        # depth = 1 # Show FK's every values, not only id

    def get_average_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]

        return room.owner == request.user

class RoomDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_average_rating(self, room):

        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]

        return room.owner == request.user
