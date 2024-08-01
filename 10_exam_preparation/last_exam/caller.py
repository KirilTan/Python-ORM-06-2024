import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg
from main_app.models import Author, Article


# Create queries within functions
def get_authors(search_name: str = None, search_email: str = None) -> str:
    """
    This function retrieves authors based on the provided search criteria.

    Parameters:
        search_name (str, optional): The full name of the author to search for. Defaults to None.
        search_email (str, optional): The email of the author to search for. Defaults to None.

    Returns:
        str: A formatted string containing the details of the authors that match the search criteria.
             If no authors are found, an empty string is returned.
    """

    if search_name is None and search_email is None:
        return ''

    query = Q()
    if search_name and search_email:
        query &= Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name:
        query &= Q(full_name__icontains=search_name)
    elif search_email:
        query &= Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')
    if not authors.exists():
        return ''

    result = []
    for author in authors:
        result.append(
            f'Author: {author.full_name}, '
            f'email: {author.email}, '
            f'status: {"Banned" if author.is_banned else "Not Banned"}'
        )
    return '\n'.join(result)


def get_top_publisher() -> str:
    """
    This function retrieves the author with the highest number of published articles.

    Returns:
        str: A formatted string containing the details of the top author.
             If no authors or no articles are found, an empty string is returned.
    """

    top_publisher = Author.objects.get_authors_by_article_count().first()

    if not top_publisher or top_publisher.num_articles == 0:
        return ''

    return (
        f'Top Author: {top_publisher.full_name} '
        f'with {top_publisher.num_articles} published articles.'
    )


def get_top_reviewer() -> str:
    """
    This function retrieves the author with the highest number of published reviews.

    Parameters:
        None

    Returns:
        str: A formatted string containing the details of the top reviewer.
             If no authors or no reviews are found, an empty string is returned.
             The string format is: "Top Reviewer: [full_name] with [num_reviews] published reviews."
    """

    top_reviewer = (
        Author.objects
        .annotate(num_reviews=Count('reviews'))
        .order_by('-num_reviews', 'email')
        .first()
    )

    if not top_reviewer or top_reviewer.num_reviews == 0:
        return ''

    return (
        f'Top Reviewer: {top_reviewer.full_name} '
        f'with {top_reviewer.num_reviews} published reviews.'
    )


def get_latest_article() -> str:
    """
    Retrieves the latest article published, along with its authors, review statistics, and average rating.

    Parameters:
        None

    Returns:
        str: A formatted string containing the details of the latest article.
             If no articles are found, an empty string is returned.
             The string format is: "The latest article is: [title]. Authors: [author_names]. Reviewed: [num_reviews] times. Average Rating: [avg_rating]."
    """

    latest_article = (
        Article.objects
        .order_by('-published_on')
        .first()
    )

    if not latest_article:
        return ""

    authors = latest_article.authors.order_by('full_name')
    author_names = ", ".join(author.full_name for author in authors)

    review_stats = latest_article.reviews.aggregate(
        num_reviews=Count('id'),
        avg_rating=Avg('rating')
    )
    num_reviews = review_stats['num_reviews'] or 0
    avg_rating = review_stats['avg_rating'] or 0

    return (
        f"The latest article is: {latest_article.title}. "
        f"Authors: {author_names}. "
        f"Reviewed: {num_reviews} times. "
        f"Average Rating: {avg_rating:.2f}."
    )


def get_top_rated_article() -> str:
    """
    Retrieves the top-rated article based on the average rating of its reviews.

    Parameters:
        None

    Returns:
        str: A formatted string containing the details of the top-rated article.
             If no articles or no reviews are found, an empty string is returned.
             The string format is: "The top-rated article is: [title], with an average rating of [avg_rating], reviewed [num_reviews] times."
    """

    top_rated_article = (
        Article.objects
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by('-avg_rating', 'title')
        .first()
    )

    if not top_rated_article or top_rated_article.avg_rating is None:
        return ""

    review_stats = top_rated_article.reviews.aggregate(
        num_reviews=Count('id')
    )
    num_reviews = review_stats['num_reviews'] or 0

    return (
        f"The top-rated article is: {top_rated_article.title}, "
        f"with an average rating of {top_rated_article.avg_rating:.2f}, "
        f"reviewed {num_reviews} times."
    )


def ban_author(email=None) -> str:
    """
    This function bans an author based on the provided email.
    If no email is provided, it returns a message indicating no authors were banned.
    If the author does not exist, it returns a message indicating no authors were banned.
    After banning the author, all their reviews are deleted.

    Parameters:
        email (str, optional): The email of the author to be banned. Defaults to None.

    Returns:
        str: A message indicating the outcome of the ban operation.
             If an email is provided and the author exists, it returns a message stating
             the author's name and the number of reviews deleted.
             If no email is provided or the author does not exist, it returns a message
             indicating no authors were banned.
    """
    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
    except Author.DoesNotExist:
        return "No authors banned."

    num_reviews = author.reviews.count()
    author.reviews.all().delete()
    author.is_banned = True
    author.save()

    return (
        f"Author: {author.full_name} is banned! "
        f"{num_reviews} reviews deleted."
    )
