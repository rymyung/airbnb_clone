from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "guests",
        "check_in",
        "check_out",
        "experience_time",
    )

    list_filter = (
        "kind",
    )
