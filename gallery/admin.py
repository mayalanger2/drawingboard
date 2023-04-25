import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Count, Min, Max, DateTimeField
from django.db.models.functions import TruncDay

from .models import Artist, Artwork, Collection, Tag, Rating, Favorite, ArtworkSummary


# Register your models here.

# This is so the changes made to the default User show up
# and are editable in the Admin's pov.

# "Define an inline admin descriptor for Artist model
# which acts a bit like a singleton"
class ArtistInline(admin.StackedInline):
    model = Artist
    can_delete = False  # this might change


# Define a new User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (ArtistInline,)


# This is for adding multiple artists to one
# Artwork submission.
class ArtworkAdmin(admin.ModelAdmin):
    model = Artwork
    # filter_horizontal = ('artwork_artist', 'artwork_tag')
    filter_horizontal = ('artwork_tag',)


# This is for adding multiple pieces of Artwork
# to the Collection.
class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    list_display = ('collection_name', 'collection_artist')


# This is for adding to pieces
# of Artwork.
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('favorite_artwork', 'favorite_artist')


# This for for displaying the Fields for Ratings.
class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating_artwork', 'rating_level', 'rating_artist')


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register other models
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Tag)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Favorite, FavoriteAdmin)


@admin.register(ArtworkSummary)
class ArtworkSummaryAdmin(admin.ModelAdmin):
    list_display = ("artwork_title", "artwork_artist", "artwork_created")

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            ArtworkSummary.objects.annotate(date=TruncDay("artwork_created"))
                .values("date")
                .annotate(y=Count("artwork_title"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    # def get_urls(self):
    # urls = super().get_urls()
    # extra_urls = [
    # path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
    # ]
    # NOTE! Our custom urls have to go before the default urls, because they
    # default ones match anything.
    # return extra_urls + urls

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return (
            ArtworkSummary.objects.annotate(date=TruncDay("artwork_created"))
                .values("date")
                .annotate(y=Count("artwork_title"))
                .order_by("-date")
        )
