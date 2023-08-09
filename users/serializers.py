from rest_framework.serializers import ModelSerializer

from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "avatar", "username")


class PrivateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "pk", "name", "username", "first_name", "last_name", "email",
            "gender", "language", "currency", "is_host"
        )
        # exclude = ("password")


# TODO: 갖고있는 house 수, 작성한 리뷰 보여주기
class PublicUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
