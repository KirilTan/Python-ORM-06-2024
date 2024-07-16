import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book


# Create queries within functions
def show_all_authors_with_their_books() -> str:
    """
    Retrieves and formats a list of authors along with the titles of the books they have written.

    This function queries all authors from the database, orders them by their ID, and for each author,
    it retrieves the books they have written. If an author has written books, it formats a string
    containing the author's name and the titles of their books, and appends this string to a list.
    Finally, it joins all the formatted strings with newline characters and returns the result.

    Returns:
        str: A formatted string where each line contains an author's name followed by the titles of the books they have written.
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


# Test functions

# Create authors
# author1 = Author.objects.create(name="J.K. Rowling")
# author2 = Author.objects.create(name="George Orwell")
# author3 = Author.objects.create(name="Harper Lee")
# author4 = Author.objects.create(name="Mark Twain")
#
# # Create books associated with the authors
# book1 = Book.objects.create(
#     title="Harry Potter and the Philosopher's Stone",
#     price=19.99,
#     author=author1
# )
# book2 = Book.objects.create(
#     title="1984",
#     price=14.99,
#     author=author2
# )
#
# book3 = Book.objects.create(
#     title="To Kill a Mockingbird",
#     price=12.99,
#     author=author3
# )
#
# # Display authors and their books
# authors_with_books = show_all_authors_with_their_books()
# print(authors_with_books)
#
# # Delete authors without books
# delete_all_authors_without_books()
# print(Author.objects.count())
# delete_everything_task_one()
