from django.contrib import admin

from .models import Amenity, Room


@admin.action(description="Set all prices to 0")
def rest_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (rest_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "amenities",
    )

    search_fields = (
        "name", # contains
        "^kind", # startswith
        "=price", # equal
        "owner__username", # FK's field
    )

    def total_amenities(self, room) -> int:
        return room.amenities.count()

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
