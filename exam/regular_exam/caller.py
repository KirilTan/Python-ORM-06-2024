import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import the models
from main_app.models import Astronaut, Spacecraft, Mission
from django.db.models import Count, Avg, Sum, Q, F, Case, When, Value, FloatField


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


def get_last_completed_mission() -> str:
    """
    Retrieves the last completed mission, including details about the commander,
    astronauts, spacecraft, and total spacewalks.

    Returns:
        str: A string containing the details of the last completed mission.
             If no completed missions exist, "No data." is returned.

    """
    last_completed_mission = (
        Mission.objects
        .filter(status='Completed')
        .order_by('-launch_date')
        .first()
    )

    if not last_completed_mission:
        return "No data."

    commander_name = last_completed_mission.commander.name if last_completed_mission.commander else "TBA"
    astronauts = last_completed_mission.astronauts.order_by('name')
    astronaut_names = ", ".join(astronaut.name for astronaut in astronauts)
    spacecraft_name = last_completed_mission.spacecraft.name
    total_spacewalks = astronauts.aggregate(total_spacewalks=Sum('spacewalks'))['total_spacewalks'] or 0

    return (
        f"The last completed mission is: {last_completed_mission.name}. "
        f"Commander: {commander_name}. "
        f"Astronauts: {astronaut_names}. "
        f"Spacecraft: {spacecraft_name}. "
        f"Total spacewalks: {total_spacewalks}."
    )


def get_most_used_spacecraft() -> str:
    """
    Retrieves the most used spacecraft in the database based on the number of missions it has been involved in.
    If multiple spacecraft have the same number of missions, the one with the earliest name is returned.
    If no spacecraft have any missions, "No data." is returned.

    Returns:
        str: A string containing the details of the most used spacecraft.
             If no data is available, "No data." is returned.
    """
    most_used_spacecraft = (
        Spacecraft.objects
        .annotate(num_missions=Count('missions'))
        .order_by('-num_missions', 'name')
        .first()
    )

    if not most_used_spacecraft or most_used_spacecraft.num_missions == 0:
        return "No data."

    num_astronauts = (
        Astronaut.objects
        .filter(missions__spacecraft=most_used_spacecraft)
        .distinct()
        .count()
    )

    return (
        f"The most used spacecraft is: {most_used_spacecraft.name}, "
        f"manufactured by {most_used_spacecraft.manufacturer}, "
        f"used in {most_used_spacecraft.num_missions} missions, "
        f"astronauts on missions: {num_astronauts}."
    )


def decrease_spacecrafts_weight() -> str:
    """
    This function decreases the weight of spacecrafts that are currently planned for missions and have a weight
    greater than or equal to 200.0 kg. The weight of each spacecraft is decreased by 200.0 kg.

    Returns:
        str: A string indicating the number of spacecrafts whose weights have been decreased and the new average weight
             of all spacecrafts. If no spacecrafts meet the criteria, a message indicating no changes is returned.
    """
    spacecrafts_to_update = (
        Spacecraft.objects
        .filter(missions__status='Planned', weight__gte=200.0)
        .distinct()
    )

    if not spacecrafts_to_update.exists():
        return "No changes in weight."

    updated_count = spacecrafts_to_update.update(
        weight=Case(
            When(weight__gte=200.0, then=F('weight') - 200.0),
            default=Value(0.0),
            output_field=FloatField()
        )
    )

    avg_weight = Spacecraft.objects.aggregate(avg_weight=Avg('weight'))['avg_weight']

    return (
        f"The weight of {updated_count} spacecrafts has been decreased. "
        f"The new average weight of all spacecrafts is {avg_weight:.1f}kg"
    )
