from django.contrib import admin

# Import the admin classes
from .admin.astronaut_admin import AstronautAdmin
from .admin.spacecraft_admin import SpacecraftAdmin
from .admin.mission_admin import MissionAdmin

# Import the models to be registered in the admin interface
from main_app.models import Astronaut, Spacecraft, Mission

# Register the models in the admin interface
admin.site.register(Astronaut, AstronautAdmin)
admin.site.register(Spacecraft, SpacecraftAdmin)
admin.site.register(Mission, MissionAdmin)
