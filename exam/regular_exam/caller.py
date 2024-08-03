import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Astronaut, Spacecraft, Mission
from django.db.models import Count, Avg, Sum, Q, F


# Create queries within functions
def get_astronauts(search_string: str = None) -> str:
    """
    This function retrieves astronauts based on a search string. If no search string is provided,
    it returns all astronauts. The search is case-insensitive and matches the search string with
    either the astronaut's name or phone number. The results are ordered by the astronaut's name.

    Parameters:
        search_string (str): The search string to filter astronauts. If None, all astronauts are returned.

    Returns:
        str: A string containing the details of the filtered astronauts. If no astronauts are found,
             an empty string is returned.
    """
    if search_string is None:
        return ""

    astronauts = Astronaut.objects.filter(
        Q(name__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by('name')

    if not astronauts.exists():
        return ""

    result = []
    for astronaut in astronauts:
        status = "Active" if astronaut.is_active else "Inactive"
        result.append(
            f'Astronaut: {astronaut.name}, '
            f'phone number: {astronaut.phone_number}, '
            f'status: {status}'
        )

    return '\n'.join(result)


def get_top_astronaut() -> str:
    """
    This function retrieves the astronaut with the highest number of missions.
    If multiple astronauts have the same number of missions, the one with the
    earliest phone number is returned. If no astronauts have any missions,
    "No data." is returned.

    Returns:
        str: A string containing the name of the top astronaut and the number of
             missions they have completed. If no data is available, "No data."
             is returned.
    """
    top_astronaut = (
        Astronaut.objects.
        annotate(
            num_of_missions=Count('missions')
        ).
        order_by(
            '-num_of_missions',
            'phone_number'
        ).
        first()
    )

    if not top_astronaut or top_astronaut.num_of_missions == 0:
        return "No data."

    return (
        f"Top Astronaut: {top_astronaut.name} "
        f"with {top_astronaut.num_of_missions} missions."
    )


def get_top_commander() -> str:
    """
    This function retrieves the astronaut with the highest number of commanded missions.
    If multiple astronauts have the same number of commanded missions, the one with the
    earliest phone number is returned. If no astronauts have any commanded missions,
    "No data." is returned.

    Returns:
        str: A string containing the name of the top commander and the number of
             commanded missions they have completed. If no data is available, "No data."
             is returned.

    """
    top_commander = (
        Astronaut.objects
        .annotate(
            num_of_commanded_missions=Count('commanded_missions')
        )
        .order_by(
            '-num_of_commanded_missions',
            'phone_number'
        )
        .first()
    )

    if not top_commander or top_commander.num_of_commanded_missions == 0:
        return "No data."

    return (
        f"Top Commander: {top_commander.name} "
        f"with {top_commander.num_of_commanded_missions} commanded missions."
    )
