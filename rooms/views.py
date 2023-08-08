from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import NotAuthenticated, NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer

from .models import Amenity, Room
from .serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer

"""
GET /api/v1/tweets                          o
POST /api/v1/tweets                         o
GET /api/v1/tweets/<int:pk>                 o
PUT /api/v1/tweets/<int:pk>                 x
DELETE /api/v1/tweets/<int:pk>              o
GET /api/v1/users                           o
GET /api/v1/users/<int:pk>                  o
GET /api/v1/users/<int:pk>/tweets           o
"""

class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):

    def get_object(self, pk: int):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk: int):
        amenity = self.get_object(pk=pk)
        return Response(AmenitySerializer(amenity).data)

    def put(self, request, pk: int):
        amenity = self.get_object(pk=pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk: int):
        amenity = self.get_object(pk=pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():

            category_id = request.data.get("category")
            if not category_id:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_id)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be rooms.")
            except Category.DoesNotExist:
                raise ParseError("Category is not found.")

            try:
                with transaction.atomic():
                    room = serializer.save(owner=request.user, category=category)

                    amenities = request.data.get("amenities")
                    for amenity_id in amenities:
                        amenity = Amenity.objects.get(pk=amenity_id)
                        room.amenities.add(amenity)

                    return Response(RoomDetailSerializer(room).data)
            except Exception:
                raise ParseError("Amenity not found.")
        else:
            return Response(serializer.errors)


class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk: int):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk: int):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk: int):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_room = serializer.save()
            return Response(RoomDetailSerializer(updated_room).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk: int):

        room = self.get_object(pk)

        if not request.user.is_authenticated:
            raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied

        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    def get_object(self, pk: int):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk: int):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk=pk)
        serializer = ReviewSerializer(room.reviews.all()[start:end], many=True)

        return Response(serializer.data)


class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk: int):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk: int):
        room = self.get_object(pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            return Response(PhotoSerializer(photo).data)
        else:
            return Response(serializer.errors)
