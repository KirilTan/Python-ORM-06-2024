from django.contrib import admin

from main_app.models import Mission

from .base_admin import BaseAdmin


@admin.register(Mission)
class MissionAdmin(BaseAdmin):
    """
    Custom admin interface for Mission model.

    This class provides customizations for the Mission model in the Django admin interface.
    It includes list display, list filtering, and search fields for the Mission model.

    Attributes:
        - list_display: A list of field names to display in the list view of the Mission model.
        - list_filter: A list of field names to use as filters in the list view of the Mission model.
        - search_fields: A list of field names to use as search fields in the list view of the Mission model.
    """

    list_display = [
        'name',
        'status',
        'description',
        'launch_date',
    ]

    list_filter = [
        'status',
        'launch_date',
    ]

    search_fields = [
        'commander__name',
    ]

