import os
import django
from django.db.models import Q, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Profile, Product, Order


# Create queries within functions
def create_profile(full_name, email, phone_number, address):
    """
    Creates a new profile and saves it in the database.

    Parameters:
        full_name (str): The full name of the profile.
        email (str): The email of the profile.
        phone_number (str): The phone number of the profile.
        address (str): The address of the profile.

    Returns:
        str: A message indicating the successful creation of the profile with the provided details.
    """
    Profile.objects.create(full_name=full_name,
                           email=email,
                           phone_number=phone_number,
                           address=address)
    return (f"{full_name} profile created successfully with:\n"
            f"  --email: {email}\n"
            f"  --phone_number: {phone_number}\n"
            f"  --address: {address}")


def create_product(name, description, price, in_stock):
    """
    Creates a new product and saves it in the database.

    Parameters:
        name (str): The name of the product.
        description (str): A detailed description of the product.
        price (float): The price of the product.
        in_stock (bool): Indicates whether the product is currently in stock.

    Returns:
        str: A message indicating the successful creation of the product with the provided details.
    """
    Product.objects.create(name=name,
                           description=description,
                           price=price,
                           in_stock=in_stock)
    return (f"{name} product created successfully with:\n"
            f"  --description: {description}\n"
            f"  --price: {price}\n"
            f"  --in_stock: {in_stock}")


def create_order(profile_id, products, total_price):
    """
    Creates a new order and saves it in the database.

    Parameters:
        profile_id (int): The unique identifier of the profile associated with the order.
        products (list): A list of Product objects associated with the order.
        total_price (float): The total price of the order.

    Returns:
        str: A message indicating the successful creation of the order with the provided details.
    """
    profile = Profile.objects.get(id=profile_id)
    order = Order.objects.create(profile=profile,
                                 total_price=total_price)
    for product in products:
        order.products.add(product)

    return (f"Order created successfully with:\n"
            f"  --profile_id: {profile_id}\n"
            f"  --total_price: {total_price}")


def get_profiles(search_string: str = None) -> str:
    """
    Retrieves profiles based on a search string and returns a formatted string of matching profiles.

    Parameters:
        search_string (str): The string to search for in full name, email, or phone number.
                             If not provided, all profiles will be returned.

    Returns:
        str: A newline-separated string of profiles that match the search string.
            Each profile is represented by its full name, email, phone number, and order count.
            If no profiles match the search criteria, an empty string is returned.
    """
    # If no search string is provided, return an empty string
    if search_string is None:
        return ""

    # Get profiles that match the search string in full name, email, or phone number,
    # and annotate the count of orders for each profile. Order the results by full name.
    matching_profiles = (
        Profile.objects.
        annotate(
            order_count=Count('orders')
        )
        .filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)
        ).
        order_by(
            'full_name'
        )
    )

    # Create return string with newline-separated profiles
    return_string = []
    for profile in matching_profiles:
        return_string.append(
            f'Profile: {profile.full_name}, '
            f'email: {profile.email}, '
            f'phone number: {profile.phone_number}, '
            f'orders: {profile.order_count}'
        )

    # Return empty string if no orders fit the search criteria
    if not return_string:
        return ''

    # Return formatted string with newline-separated profiles
    return '\n'.join(return_string)


def get_loyal_profiles() -> str:
    """
    Retrieves regular customers who have placed more than 2 orders.

    Returns:
    str: A newline-separated string of loyal profiles and their order counts.
        Each profile is represented by its full name and the number of orders placed.
        If no loyal profiles are found, an empty string is returned.
    """
    # Get regular customers who have placed more than 2 orders.
    loyal_profiles = Profile.objects.get_regular_customers()

    # Return an empty string if no loyal profiles found
    if not loyal_profiles:
        return ""

    # Create return string with newline-separated loyal profiles and their order counts
    result = []
    for profile in loyal_profiles:
        result.append(
            f"Profile: {profile.full_name}, "
            f"orders: {profile.order_count}"
        )

    # Return formatted string with newline-separated loyal profiles
    return '\n'.join(result)


def get_last_sold_products() -> str:
    """
    Retrieves the names of the products sold in the most recent order.

    Returns:
        str: A string representing the names of the last sold products.
            If no orders or products exist, an empty string is returned.
            The product names are comma-separated and ordered alphabetically.
    """
    # Retrieve the most recent order
    latest_order = Order.objects.order_by('-creation_date').first()

    # Check if an order exists and if it has any associated products
    if not latest_order or not latest_order.products.exists():
        return ""

    # Retrieve the products associated with the most recent order and order them by name
    products = latest_order.products.order_by('name')

    # Create a comma-separated string of product names
    product_names = ', '.join(product.name for product in products)

    # Return the formatted string of product names
    return f"Last sold products: {product_names}"
