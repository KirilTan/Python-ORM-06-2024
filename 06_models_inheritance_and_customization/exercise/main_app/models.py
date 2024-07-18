from django.db import models


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
