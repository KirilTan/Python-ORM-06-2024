import os
import django

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


# # Create some sample data
# # Create some profiles
# create_profile("John Doe", "johndoe@example.com", "+359899999999", "123 Main St, City")
# create_profile("Jane Smith", "janesmith@example.com", "+359899999999", '456 Elm St, City')
# # Create some products
# create_product("Product A", "This is Product A.", 19.99, True)
# create_product("Product B", "This is Product B.", 29.99, False)
# create_product("Product C", "This is Product C.", 39.99, True)
# # Create some orders
# create_order(1, [Product.objects.get(id=1), Product.objects.get(id=2)], 59.98)
