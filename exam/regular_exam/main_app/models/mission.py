from django.db import models
from .base import TimeStampedMixin, NamedMixin
from .choices import MissionStatusChoices
from .astronaut import Astronaut
from .spacecraft import Spacecraft


class Mission(NamedMixin, TimeStampedMixin):
    """
    A model representing a space mission.

    Attributes:
        description (TextField): A brief description of the mission.
        status (CharField): The current status of the mission.
        launch_date (DateField): The planned launch date of the mission.
        spacecraft (ForeignKey): The spacecraft associated with the mission.
        astronauts (ManyToManyField): The astronauts participating in the mission.
        commander (ForeignKey): The commander of the mission.
    """

    description = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=9,
        choices=MissionStatusChoices.CHOICES,
        default=MissionStatusChoices.PLANNED,
    )

    launch_date = models.DateField()

    spacecraft = models.ForeignKey(
        to=Spacecraft,
        on_delete=models.CASCADE,
        related_name='missions',
    )

    astronauts = models.ManyToManyField(
        to=Astronaut,
        related_name='missions',
    )

    commander = models.ForeignKey(
        to=Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commanded_missions',
    )
