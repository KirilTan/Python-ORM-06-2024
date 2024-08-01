import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count
from main_app.models import Author


# Create queries within functions
def get_authors(search_name: str = None, search_email: str = None) -> str:

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
    top_publisher = Author.objects.get_authors_by_article_count().first()

    if not top_publisher or top_publisher.num_articles == 0:
        return ''

    return (
        f'Top Author: {top_publisher.full_name} '
        f'with {top_publisher.num_articles} published articles.'
    )


def get_top_reviewer() -> str:
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