import os
from pprint import pprint

import django
from django.db import connection
from django.db.models import Sum, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct


# Create and run queries
def add_records_to_database():
    # Categories
    food_category = Category.objects.create(name='Food')
    drinks_category = (Category.objects.create(name='Drinks'))

    # Food
    product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99,
                                      category=food_category, is_available=False)
    product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99,
                                      category=food_category, is_available=False)
    product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99,
                                      category=food_category, is_available=True)
    product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49,
                                      category=food_category, is_available=True)
    product5 = Product.objects.create(name='Pasta and Sauce Bundle',
                                      description='Package containing pasta and a jar of pasta sauce', price=6.99,
                                      category=food_category, is_available=False)
    product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99,
                                      category=food_category, is_available=True)
    product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs',
                                      price=3.49, category=food_category, is_available=True)
    product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99,
                                      category=food_category, is_available=False)
    product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49,
                                      category=food_category, is_available=True)

    # Drinks
    product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99,
                                       category=drinks_category, is_available=True)
    product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49,
                                       category=drinks_category, is_available=False)
    product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water',
                                       price=4.99, category=drinks_category, is_available=True)
    product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49,
                                       category=drinks_category, is_available=True)
    product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99,
                                       category=drinks_category, is_available=False)
    product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49,
                                       category=drinks_category, is_available=True)

    # Customers
    customer1 = Customer.objects.create(username='john_doe')
    customer2 = Customer.objects.create(username='alex_alex')
    customer3 = Customer.objects.create(username='peter132')
    customer4 = Customer.objects.create(username='k.k.')
    customer5 = Customer.objects.create(username='peter_smith')

    # Orders
    order1 = Order.objects.create(customer=customer1)
    order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
    order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
    order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
    order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)

    order2 = Order.objects.create(customer=customer3)
    order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
    order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)

    order3 = Order.objects.create(customer=customer1)
    order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
    order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
    return "All data entered!"


# Run and print your queries
# print(add_records_to_database())

def product_quantity_ordered() -> str:
    """
    Retrieves and returns a string representation of the total quantity ordered for each product, 
    sorted in descending order of quantity.

    Returns:
        str: A string where each line contains the product name and the total quantity ordered 
             for that product, sorted by the total quantity in descending order.
    """
    total_products_ordered = (
        Product.objects
        .annotate(total_ordered_quantity=Sum('orderproduct__quantity'))
        .exclude(total_ordered_quantity=None)
        .order_by('-total_ordered_quantity')
    )

    result = []
    for product in total_products_ordered:
        result.append(
            f'Quantity ordered of {product.name}: {product.total_ordered_quantity}'
        )
    return '\n'.join(result)


def ordered_products_per_customer() -> str:
    """
    Retrieves and returns a string representation of all orders, including the customer who placed the order 
    and the products in each order, along with their categories.

    Returns:
        str: A string where each order is listed with its ID and the username of the customer who placed it. 
             Each product in the order is listed with its name and category.
    """
    prefetched_orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

    result = []
    for order in prefetched_orders:
        result.append(
            f'Order ID: {order.id}, Customer: {order.customer.username}'
        )

        for order_product in order.orderproduct_set.all():
            result.append(
                f'- Product: {order_product.product.name}, Category: {order_product.product.category.name}'
            )

    return '\n'.join(result)


def filter_products() -> str:
    """
    Filters and retrieves products that are available and have a price greater than 3.00,
    then sorts them by price in descending order and by name in ascending order.

    Returns:
        str: A string representation of the filtered products, where each line contains the 
             product name and its price, formatted as 'Product Name: Price lv.'.
    """
    query = Q(is_available=True) & Q(price__gt=3.00)
    products = (Product.objects
                .filter(query)
                .order_by('-price',
                          'name')
                )

    result = []
    for product in products:
        result.append(
            f'{product.name}: {product.price}lv.'
        )

    return '\n'.join(result)


def give_discount():
    """
    Applies a 30% discount to all available products with a price greater than 3.00,
    then retrieves and returns a string representation of all available products sorted by price in descending order 
    and by name in ascending order.

    Returns:
        str: A string where each line contains the product name and its discounted price, formatted as 'Product Name: Price lv.'.
    """
    reduction = F('price') * 0.7
    query = Q(is_available=True) & Q(price__gt=3.00)

    (Product.objects
     .filter(query)
     .update(price=reduction))

    all_available_products = (
        Product.objects
        .filter(is_available=True)
        .order_by('-price',
                  'name')
    )

    result = []
    for product in all_available_products:
        result.append(
            f'{product.name}: {product.price}lv.'
        )

    return '\n'.join(result)


# Print sql queries executed
# print('\n',
#       '-' * 100,
#       '\n')
# pprint(connection.queries)
