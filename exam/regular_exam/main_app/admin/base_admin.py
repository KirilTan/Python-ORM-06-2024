from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Custom Django ModelAdmin class with predefined settings.

    This class extends the functionality of Django's built-in ModelAdmin class by
    setting default values for readonly_fields and ordering attributes.

    Attributes:
        readonly_fields: A list of field names that should be displayed as read-only in the admin interface.
        ordering: A list of field names that determines the default ordering of objects in the admin interface.

    Methods:
        None
    """

    readonly_fields = [
        'updated_at',
    ]

    ordering = [
        'name',
    ]