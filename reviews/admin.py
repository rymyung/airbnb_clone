from django.contrib import admin

from .models import Review


class WordFilter(admin.SimpleListFilter):

    title = "Filter by words!"

    parameter_name = "filtering_word"

    def lookups(self, request, model_admin):
        return [
            ("great", "Great"),
            ("good", "Good"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        filtering_word = self.value()
        if filtering_word:
            return reviews.filter(payload__contains=filtering_word)
        else:
            return reviews


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        "rating",
        "user__is_host", # FK's field
        "room__category", # FK's field
    )
