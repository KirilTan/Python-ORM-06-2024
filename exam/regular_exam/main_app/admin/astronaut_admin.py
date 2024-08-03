from django.contrib import admin

from main_app.models import Astronaut

from .base_admin import BaseAdmin


@admin.register(Astronaut)
class AstronautAdmin(BaseAdmin):
    """
    Custom admin interface for the Astronaut model.

    This class extends the BaseAdmin class and provides customizations for the Astronaut model in the Django admin interface.

    Attributes:
        - list_display: A list of field names to display in the list view of the Astronaut model in the admin interface.
        - list_filter: A list of field names to use as filters in the list view of the Astronaut model in the admin interface.
        - search_fields: A list of field names to use as search fields in the list view of the Astronaut model in the admin interface.
    """

    list_display = [
        'name',
        'spacewalks',
        'is_active',
    ]

    list_filter = [
        'is_active',
    ]

    search_fields = [
        'name',
        'phone_number',
    ]