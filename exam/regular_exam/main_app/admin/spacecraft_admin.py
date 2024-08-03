from django.contrib import admin

from main_app.models import Spacecraft

from .base_admin import BaseAdmin


@admin.register(Spacecraft)
class SpacecraftAdmin(BaseAdmin):
    """
     Custom admin interface for the Spacecraft model.

    This class extends the BaseAdmin class and provides customizations for the
    Django admin interface for the Spacecraft model. It defines the fields to be
    displayed in the list view, filters to be applied, and search fields.

    Attributes:
        - list_display: A list of field names to display in the list view of the Spacecraft model.
        - list_filter: A list of field names to use as filters in the list view of the Spacecraft model.
        - search_fields: A list of field names to use as search fields in the list view of the Spacecraft model.

    """
    list_display = [
        'name',
        'manufacturer',
        'launch_date',
    ]

    list_filter = [
        'capacity',
    ]

    search_fields = [
        'name',
    ]

