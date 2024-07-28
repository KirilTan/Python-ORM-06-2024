from django.db import models
from django.core import validators
from django.db.models import Count


# Mixins
class CreationDateMixin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


# Custom managers
class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return self.annotate(order_count=Count('orders')).filter(order_count__gt=2).order_by('-order_count')


# Models
class Profile(CreationDateMixin, IsActiveMixin):
    full_name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(
                limit_value=2,
                message='Full name must be at least 2 characters long.'
            ),
        ],
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
    )
    address = models.TextField()

    objects = ProfileManager()


class Product(CreationDateMixin):
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(
                limit_value=0.01,
                message='Price must be a positive number.'
            )
        ]
    )
    in_stock = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(
                limit_value=0,
                message='Stock cannot be negative.'
            )
        ]
    )
    is_available = models.BooleanField(
        default=True,
    )


class Order(CreationDateMixin):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(
                limit_value=0.01,
                message='Total price must be a positive number.'
            )
        ]
    )
    is_completed = models.BooleanField(
        default=False,
    )
