import os
from datetime import timedelta, date

import django
from django.db.models import QuerySet, Sum, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Registration, \
    Car


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    """
    Retrieves and formats a list of authors along with the titles of the books they have written.

    This function queries all authors from the database, orders them by their ID, and for each author,
    it retrieves the books they have written. If an author has written books, it formats a string
    containing the author's name and the titles of their books, and appends this string to a list.
    Finally, it joins all the formatted strings with newline characters and returns the result.

    Returns:
        str: A formatted string where each line contains an author's name
             followed by the titles of the books they have written.
    """
    authors_books = []

    authors = Author.objects.all().order_by('id')
    for author in authors:
        books = author.books.all()

        if not books:
            continue

        titles = ', '.join(book.title for book in books)

        authors_books.append(
            f"{author.name} has written - {titles}!"
        )

    return '\n'.join(authors_books)


def delete_all_authors_without_books() -> None:
    """
    Deletes all authors from the database who do not have any associated books.

    This function queries the Author model to find all authors who do not have any books
    associated with them (i.e., authors for whom the 'books' relationship is null) and deletes them.

    Returns:
        None
    """
    Author.objects.filter(books__isnull=True).delete()


def delete_everything_task_one() -> None:
    """
    Deletes all records from the Author and Book models in the database.

    This function performs a complete deletion of all entries in the Author and Book tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Author.objects.all().delete()
    Book.objects.all().delete()


def add_song_to_artist(artist_name: str, song_title: str) -> None:
    """
    Adds a song to an artist's list of songs.

    This function retrieves an artist and a song from the database based on their names,
    and then associates the song with the artist.

    Args:
        artist_name (str): The name of the artist to whom the song will be added.
        song_title (str): The title of the song to be added to the artist's list of songs.

    Returns:
        None
    """
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str) -> QuerySet[Song]:
    """
    Retrieves a list of songs associated with a given artist, ordered by their ID in descending order.

    Args:
        artist_name (str): The name of the artist whose songs are to be retrieved.

    Returns:
        QuerySet[Song]: A queryset containing the songs associated with the specified artist,
                        ordered by their ID in descending order.
    """
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str) -> None:
    """
    Removes a song from an artist's list of songs.

    This function retrieves an artist and a song from the database based on their names,
    and then disassociates the song from the artist.

    Args:
        artist_name (str): The name of the artist from whom the song will be removed.
        song_title (str): The title of the song to be removed from the artist's list of songs.

    Returns:
        None
    """
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def delete_everything_task_two() -> None:
    """
    Deletes all records from the Artist and Song models in the database.

    This function performs a complete deletion of all entries in the Artist and Song tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Artist.objects.all().delete()
    Song.objects.all().delete()


def calculate_average_rating_for_product_by_name(product_name: str) -> float:
    """
    Calculates the average rating for a product based on its reviews.

    This function retrieves a product by its name and calculates the average rating
    from all associated reviews.

    Args:
        product_name (str): The name of the product for which the average rating is to be calculated.

    Returns:
        float: The average rating of the product based on its reviews.
    """
    product = Product.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).get(
        name=product_name
    )
    return product.avg_rating


def get_reviews_with_high_ratings(threshold: int) -> QuerySet[Review]:
    """
    Retrieves a list of reviews with ratings greater than or equal to the specified threshold.

    This function queries the Review model to find all reviews that have a rating greater than or equal
    to the given threshold.

    Args:
        threshold (int): The minimum rating value to filter reviews.

    Returns:
        QuerySet[Review]: A queryset containing the reviews with ratings greater than or equal to the threshold.
    """
    reviews = Review.objects.filter(rating__gte=threshold)
    return reviews


def get_products_with_no_reviews() -> QuerySet[Product]:
    """
    Retrieves a list of products that do not have any associated reviews.

    This function queries the Product model to find all products that do not have any reviews
    associated with them (i.e., products for which the 'reviews' relationship is null) and orders
    them by their name in descending order.

    Returns:
        QuerySet[Product]: A queryset containing the products with no reviews, ordered by their name in descending order
    """
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews() -> None:
    """
    Deletes all products from the database that do not have any associated reviews.

    This function queries the Product model to find all products that do not have any reviews
    associated with them (i.e., products for which the 'reviews' relationship is null) and deletes them.

    Returns:
        None
    """
    Product.objects.filter(reviews__isnull=True).delete()


def delete_everything_task_three() -> None:
    """
    Deletes all records from the Product and Review models in the database.

    This function performs a complete deletion of all entries in the Product and Review tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Product.objects.all().delete()
    Review.objects.all().delete()


def calculate_licenses_expiration_dates() -> str:
    """
    Calculates the expiration dates for all driving licenses and formats them into a string.

    This function retrieves all drivers from the database, orders them by their license number in descending order,
    and calculates the expiration date for each license (one year from the issue date). It then formats a string
    containing the license number and its expiration date for each driver and appends this string to a list.
    Finally, it joins all the formatted strings with newline characters and returns the result.

    Returns:
        str: A formatted string where each line contains a license number and its expiration date.
    """
    output = []

    for driver in Driver.objects.all().order_by('-license__license_number'):
        output.append(
            f"License with number: {driver.license.license_number} "
            f"expires on {driver.license.issue_date + timedelta(days=365)}!"
        )

    return '\n'.join(output)


def get_drivers_with_expired_licenses(due_date: date) -> QuerySet[Driver]:
    """
    Retrieves a list of drivers whose licenses have expired by a given due date.

    This function calculates the expiration cutoff date by subtracting one year from the provided due date.
    It then queries the Driver model to find all drivers whose license issue date is greater than the calculated
    expiration cutoff date, indicating that their licenses have expired.

    Args:
        due_date (date): The date by which to check for expired licenses.

    Returns:
        QuerySet[Driver]: A queryset containing the drivers with expired licenses.
    """
    expiration_cutoff_date = due_date - timedelta(days=365)
    drivers_with_expired_licenses = Driver.objects.filter(
        license__issue_date__gt=expiration_cutoff_date,
    )

    return drivers_with_expired_licenses


def delete_everything_task_four() -> None:
    """
    Deletes all records from the Driver and DrivingLicense models in the database.

    This function performs a complete deletion of all entries in the Driver and DrivingLicense tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Driver.objects.all().delete()
    DrivingLicense.objects.all().delete()


def register_car_by_owner(owner: Owner) -> str:
    """
    Registers a car to an owner by associating the first available car and registration.

    This function finds the first available car and registration that are not yet associated with each other.
    It then assigns the car to the given owner and sets the registration date to the current date.

    Args:
        owner (Owner): The owner to whom the car will be registered.

    Returns:
        str: A message indicating the success of the registration process, including the car model,
             owner's name, and registration number. If no car or registration is available, an appropriate
             message is returned.
    """
    # First registration that is not related to any car
    registration = Registration.objects.filter(car__isnull=True).first()

    # First car without registration
    car = Car.objects.filter(registration__isnull=True).first()

    # Check if car and registration are available
    if not registration and not car:
        return 'No car and registration available'
    elif not car:
        return 'No car available'
    elif not registration:
        return 'No registration available'

    # Set car owner
    car.owner = owner
    car.save()

    # Set registration date
    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    # Output message
    message = (f'Successfully registered {car.model} '
               f'to {owner.name} '
               f'with registration number {registration.registration_number}.')
    return message


def delete_everything_task_five() -> None:
    """
    Deletes all records from the Owner, Car, and Registration models in the database.

    This function performs a complete deletion of all entries in the Owner, Car, and Registration tables.
    It does not take any parameters and does not return any value.

    Returns:
        None
    """
    Owner.objects.all().delete()
    Car.objects.all().delete()
    Registration.objects.all().delete()


# Test functions
