from decimal import Decimal

from django.core.validators import RegexValidator, MinValueValidator, MinLengthValidator
from django.db import models

from main_app.mixins import RechargeEnergyMixin


# Create your models here.
class Customer(models.Model):
    """
    Represents a customer with personal and contact information.

    Attributes:
        name (str): The name of the customer. Must contain only letters and spaces.
        age (int): The age of the customer. Must be 18 or older.
        email (str): The email address of the customer. Must be a valid email format.
        phone_number (str): The phone number of the customer. Must start with '+359' followed by 9 digits.
        website_url (str): The website URL of the customer. Must be a valid URL format.
    """

    name = models.CharField(
        max_length=100,
        validators=
        [
            RegexValidator
            (
                regex=r'^[a-zA-Z\s]+$',
                message='Name can only contain letters and spaces',
            )
        ],
    )

    age = models.PositiveIntegerField(
        validators=
        [
            MinValueValidator
            (
                limit_value=18,
                message='Age must be greater than or equal to 18'
            ),
        ],
    )

    email = models.EmailField(
        error_messages=
        {
            'invalid': "Enter a valid email address"
        }
    )

    phone_number = models.CharField(
        max_length=13,
        validators=
        [
            RegexValidator
            (
                regex=r'^\+359\d{9}$',
                message="Phone number must start with '+359' followed by 9 digits",
            )
        ],
    )

    website_url = models.URLField(
        error_messages=
        {
            'invalid': "Enter a valid URL"
        }
    )


class BaseMedia(models.Model):
    """
    Abstract base class for media items such as books, movies, and music.

    Attributes:
        title (str): The title of the media item.
        description (str): A detailed description of the media item.
        genre (str): The genre of the media item.
        created_at (datetime): The date and time when the media item was created.
    """

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    genre = models.CharField(
        max_length=50,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = [
            '-created_at',
            'title',
        ]


class Book(BaseMedia):
    """
    Represents a book with specific attributes such as author and ISBN.

    Attributes:
        author (str): The author of the book. Must be at least 5 characters long.
        isbn (str): The ISBN of the book. Must be unique and at least 6 characters long.
    """
    author = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=5,
                message='Author must be at least 5 characters long'
            )
        ]
    )

    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(
                limit_value=6,
                message='ISBN must be at least 6 characters long'
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'


class Movie(BaseMedia):
    """
    Represents a movie with specific attributes such as director.

    Attributes:
        director (str): The director of the movie. Must be at least 8 characters long.
    """
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=8,
                message='Director must be at least 8 characters long'
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=
        [
            MinLengthValidator
            (
                limit_value=9,
                message='Artist must be at least 9 characters long'
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'

    def get_artist_info(self) -> str:
        """
        Retrieves the artist information for the music item.

        Returns:
            str: A string containing the artist's name.
        """
        return f'Artist: {self.artist}'


class Product(models.Model):
    name = models.CharField(
        max_length=100,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self) -> Decimal:
        """
        Calculate the tax for the product based on a fixed tax rate.

        Returns:
            Decimal: The calculated tax amount for the product.
        """
        tax_rate = Decimal(0.08)
        price = self.price * tax_rate
        return price

    @staticmethod
    def calculate_shipping_cost(weight: Decimal) -> Decimal:
        """
        Calculate the shipping cost based on the weight of the product.

        Args:
            weight (Decimal): The weight of the product.

        Returns:
            Decimal: The calculated shipping cost.
        """
        multiplier = Decimal(2)
        shipping_cost = weight * multiplier
        return shipping_cost

    def format_product_name(self) -> str:
        """
        Format the product name for display.

        Returns:
            str: The formatted product name.
        """
        text = f'Product: {self.name}'
        return text


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        """
        Calculate the original price of the product before applying the discount.

        Returns:
            Decimal: The original price of the product before the discount.
        """
        percentage_higher = Decimal(0.2)
        price_without_discount = self.price * (1 + percentage_higher)
        return price_without_discount

    def calculate_tax(self) -> Decimal:
        """
        Calculate the tax for the discounted product based on a fixed tax rate.

        Returns:
            Decimal: The calculated tax amount for the discounted product.
        """
        tax_rate = Decimal(0.05)
        tax_for_product = self.price * tax_rate
        return tax_for_product

    @staticmethod
    def calculate_shipping_cost(weight: Decimal) -> Decimal:
        """
        Calculate the shipping cost based on the weight of the discounted product.

        Args:
            weight (Decimal): The weight of the product.

        Returns:
            Decimal: The calculated shipping cost.
        """
        multiplier = Decimal(1.5)
        shipping_cost = weight * multiplier
        return shipping_cost

    def format_product_name(self) -> str:
        """
        Format the product name for display, indicating it is a discounted product.

        Returns:
            str: The formatted product name.
        """
        text = f'Discounted Product: {self.name}'
        return text


class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(
        max_length=100
    )

    hero_title = models.CharField(
        max_length=100
    )

    energy = models.PositiveIntegerField()  # Needs to always be a positive integer

    def use_energy(self, expenditure: int, success_message: str, failure_message: str) -> str:
        """
        Manages the energy expenditure of the hero and returns an appropriate message based on the result.

        Args:
            expenditure (int): The amount of energy to be used.
            success_message (str): The message to return if the energy expenditure is successful.
            failure_message (str): The message to return if there is not enough energy.

        Returns:
            str: A success message if the hero has enough energy, otherwise a failure message.
        """
        new_energy = self.energy - expenditure

        if new_energy < 0:
            return failure_message

        elif new_energy == 0:
            self.energy = 1

        else:
            self.energy = new_energy

        self.save()
        return success_message


class SpiderHero(Hero):
    def swing_from_buildings(self) -> str:
        """
        Simulates the Spider Hero swinging from buildings using web shooters.

        This function attempts to use a specified amount of energy for the action.
        If successful, it returns a success message; otherwise, it returns a failure message.

        Returns:
            str: A message indicating whether the action was successful or if the hero is out of web shooter fluid.
        """
        expenditure = 80
        success_message = f'{self.name} as Spider Hero swings from buildings using web shooters'
        failure_message = f'{self.name} as Spider Hero is out of web shooter fluid'
        return self.use_energy(expenditure, success_message, failure_message)

    class Meta:
        proxy = True


class FlashHero(Hero):
    def run_at_super_speed(self) -> str:
        """
        Simulates the Flash Hero running at super speed.

        This function attempts to use a specified amount of energy for the action.
        If successful, it returns a success message; otherwise, it returns a failure message.

        Returns:
            str: A message indicating whether the action was successful or if the hero needs to recharge.
        """
        expenditure = 65
        success_message = f'{self.name} as Flash Hero runs at lightning speed, saving the day'
        failure_message = f'{self.name} as Flash Hero needs to recharge the speed force'
        return self.use_energy(expenditure, success_message, failure_message)

    class Meta:
        proxy = True

