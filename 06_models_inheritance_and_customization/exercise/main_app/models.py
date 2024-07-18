from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError

from main_app.custom_fields import StudentIDField, MaskedCreditCardField


# Create your models here.
class BaseCharacter(models.Model):
    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(
        max_length=100,
    )

    spellbook_type = models.CharField(
        max_length=100,
    )


class Assassin(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    assassination_technique = models.CharField(
        max_length=100,
    )


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(
        max_length=100,
    )

    demon_slaying_ability = models.CharField(
        max_length=100,
    )


class TimeMage(Mage):
    time_magic_mastery = models.CharField(
        max_length=100,
    )

    temporal_shift_ability = models.CharField(
        max_length=100,
    )


class Necromancer(Mage):
    raise_dead_ability = models.CharField(
        max_length=100,
    )


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(
        max_length=100,
    )

    venomous_bite_ability = models.CharField(
        max_length=100,
    )


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(
        max_length=100,
    )


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(
        max_length=100,
    )

    retribution_ability = models.CharField(
        max_length=100,
    )


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(
        max_length=100,
    )


class UserProfile(models.Model):
    username = models.CharField(
        max_length=70,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    bio = models.TextField(
        blank=True,
        null=True,
    )


class Message(models.Model):
    sender = models.ForeignKey(
        to=UserProfile,
        related_name='sent_messages',
        on_delete=models.CASCADE,
    )

    receiver = models.ForeignKey(
        to=UserProfile,
        related_name='received_messages',
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    is_read = models.BooleanField(
        default=False,
    )

    def mark_as_read(self) -> None:
        """
        Marks the message as read.

        This method sets the `is_read` attribute of the message to True, indicating that the message has been read.

        Returns:
            None
        """
        self.is_read = True

    def reply_to_message(self, reply_content: str) -> 'Message':
        """
        Creates a reply to the current message.
    
        This method generates a new message where the sender is the receiver of the current message,
        and the receiver is the sender of the current message. The content of the new message is
        provided by the `reply_content` parameter.
    
        Args:
            reply_content (str): The content of the reply message.
    
        Returns:
            Message: The newly created reply message instance.
        """
        new_message = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content,
        )
        return new_message

    def forward_message(self, receiver: UserProfile) -> 'Message':
        """
        Forwards the current message to a new receiver.

        This method creates a new message instance with the same content as the current message,
        but with a different receiver specified by the `receiver` parameter.

        Args:
            receiver (UserProfile): The user profile of the new receiver to whom the message will be forwarded.

        Returns:
            Message: The newly created message instance that has been forwarded to the new receiver.
        """
        new_message = Message.objects.create(
            sender=self.receiver,
            receiver=receiver,
            content=self.content,
        )
        return new_message


class Student(models.Model):
    name = models.CharField(
        max_length=100,
    )

    student_id = StudentIDField()


class CreditCard(models.Model):
    card_owner = models.CharField(
        max_length=100,
    )

    card_number = MaskedCreditCardField()


class Hotel(models.Model):
    name = models.CharField(
        max_length=100,
    )

    address = models.CharField(
        max_length=200,
    )


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    number = models.CharField(
        max_length=100,
        unique=True,
    )

    capacity = models.PositiveIntegerField()

    total_guests = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self) -> None:
        """
        Validates the Room instance to ensure that the total number of guests does not exceed the room's capacity.

        This method checks if the `total_guests` attribute is greater than the `capacity` attribute.
        If the total number of guests exceeds the room's capacity, a `ValidationError` is raised.

        Raises:
            ValidationError: If the total number of guests exceeds the room's capacity.
        """
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs) -> str:
        """
        Saves the Room instance to the database after performing validation checks.
    
        This method first calls the `clean` method to ensure that the instance is valid.
        If the instance is valid, it then calls the parent class's `save` method to save
        the instance to the database. Finally, it returns a success message.
    
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
    
        Returns:
            str: A success message indicating that the room was created successfully.
        """
        self.clean()
    
        super().save(*args, **kwargs)
    
        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):
    class Meta:
        abstract = True

    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    def reservation_period(self) -> int:
        """
        Calculates the duration of the reservation in days.

        This method computes the number of days between the start date and the end date of the reservation.

        Returns:
            int: The number of days for the reservation period.
        """
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self) -> Decimal:
        """
        Calculates the total cost of the reservation.

        This method computes the total cost by multiplying the reservation period (in days)
        by the price per night of the room. The result is rounded to two decimal places.

        Returns:
            Decimal: The total cost of the reservation, rounded to two decimal places.
        """
        total_cost = self.reservation_period() * self.room.price_per_night

        return round(total_cost, 2)

    @property
    def is_available(self) -> bool:
        """
        Checks if the room is available for the reservation period.
    
        This method queries the database to find any overlapping reservations for the same room.
        If no overlapping reservations are found, the room is considered available.
    
        Returns:
            bool: True if the room is available for the reservation period, False otherwise.
        """
        reservations = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date,
        )
    
        return not reservations.exists()

    def clean(self) -> None:
        """
        Validates the reservation instance to ensure that the start date is before the end date
        and that the room is available for the reservation period.
    
        This method performs two validation checks:
        1. Ensures that the start date is before the end date.
        2. Checks if the room is available for the specified reservation period.
    
        Raises:
            ValidationError: If the start date is not before the end date.
            ValidationError: If the room is not available for the reservation period.
        """
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")
    
        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")


class RegularReservation(BaseReservation):
    def save(self, *args, **kwargs) -> str:
        """
        Saves the RegularReservation instance to the database after performing validation checks.
    
        This method first calls the `clean` method to ensure that the instance is valid.
        If the instance is valid, it then calls the parent class's `save` method to save
        the instance to the database. Finally, it returns a success message.
    
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
    
        Returns:
            str: A success message indicating that the regular reservation was created successfully.
        """
        super().clean()
    
        super().save(*args, **kwargs)
    
        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):
    # could avoid repetition with property
    def save(self, *args, **kwargs) -> str:
        """
        Saves the SpecialReservation instance to the database after performing validation checks.
    
        This method first calls the `clean` method to ensure that the instance is valid.
        If the instance is valid, it then calls the parent class's `save` method to save
        the instance to the database. Finally, it returns a success message.
    
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
    
        Returns:
            str: A success message indicating that the special reservation was created successfully.
        """
        super().clean()
    
        super().save(*args, **kwargs)
    
        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int) -> str:
        """
        Extends the reservation period by a specified number of days.

        This method updates the end date of the reservation by adding the specified number of days.
        It then checks if the room is available for the extended period. If the room is not available,
        a ValidationError is raised. If the room is available, the reservation is saved with the new end date.

        Args:
            days (int): The number of days to extend the reservation.

        Returns:
            str: A success message indicating that the reservation was extended successfully.

        Raises:
            ValidationError: If the room is not available for the extended reservation period.
        """
        self.end_date += timedelta(days=days)

        if not self.is_available:
            raise ValidationError("Error during extending reservation")

        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"
