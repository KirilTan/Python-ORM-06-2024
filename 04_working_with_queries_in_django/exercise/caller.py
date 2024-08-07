import os
from typing import List

import django
from django.db.models import Case, When, Value, QuerySet

from main_app.choices import LaptopOperationSystemChoices, MealTypeChoices, DungeonDifficultyChoices, WorkoutTypeChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models
from main_app.models import ChessPlayer, Meal, Dungeon, Workout, ArtworkGallery, Laptop


# Create and check models
def show_highest_rated_art() -> str:
    """
    Returns a string with the highest-rated art. If two or more arts have the same rating, returns the one with the
    lowest id.

    Returns:
        str: The name of the highest-rated artwork
    """
    highest_rated_artwork = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return_string = (f"{highest_rated_artwork.art_name} is the highest-rated art "
                     f"with a {highest_rated_artwork.rating} rating!")
    return return_string


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    """
    Bulk creates two new instances of the 'ArtworkGallery' class and saves them into the database.

    Parameters:
        first_art (ArtworkGallery): The first artwork to be created
        second_art (ArtworkGallery): The second artwork to be created
    Returns:
        None
    """
    ArtworkGallery.objects.bulk_create([first_art, second_art])


def delete_negative_rated_arts() -> None:
    """
    Deletes all arts that have a rating less than 0.
    """
    artworks_to_delete = ArtworkGallery.objects.filter(rating__lt=0)

    artworks_to_delete.delete()


def show_the_most_expensive_laptop() -> str:
    """
    Returns a string with the most expensive laptop. If two or more laptops share the same price, returns the one
    with the highest id.

    Returns:
        str: The most expensive laptop
    """
    most_expensive_laptop = Laptop.objects.order_by('-price', '-id').first()
    return_string = (f"{most_expensive_laptop.brand} is the most expensive laptop "
                     f"available for {most_expensive_laptop.price}$!")
    return return_string


def bulk_create_laptops(args: List[Laptop]) -> None:
    """
    Bulk creates one or more new instances of the "Laptop" class and saves them into the database.

    Parameters:
        args (List[Laptop]): A list of Laptop instances to be created
    """
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    """
    Updates the storage for all the "Asus" and "Lenovo" laptops to 512 GB.
    """
    laptops_to_update = Laptop.objects.filter(brand__in=('Asus', 'Lenovo'))
    laptops_to_update.update(storage=512)


def update_to_16_GB_memory() -> None:
    """
    Updates the memory for all the "Apple", "Dell", and "Acer" laptops to 16 GB.
    """
    laptops_to_update = Laptop.objects.filter(brand__in=('Apple', 'Dell', 'Acer'))
    laptops_to_update.update(memory=16)


def update_operation_systems() -> None:
    """
    Updates the operating system for every laptop

    • If the brand is "Asus", update the operating system to "Windows".
    • If the brand is "Apple", update the operating system to "MacOS".
    • If the brand is "Dell" or "Acer", update the operating system to "Linux".
    • If the brand is "Lenovo", update the operating system to "Chrome OS".
    """
    brand_os_mapper = {
        'Asus': LaptopOperationSystemChoices.WINDOWS,
        'Apple': LaptopOperationSystemChoices.MACOS,
        'Dell': LaptopOperationSystemChoices.LINUX,
        'Acer': LaptopOperationSystemChoices.LINUX,
        'Lenovo': LaptopOperationSystemChoices.CHROME_OS,
    }

    for brand, laptop_os in brand_os_mapper.items():
        Laptop.objects.filter(brand=brand).update(operation_system=laptop_os)


def delete_inexpensive_laptops() -> None:
    """
    Deletes all laptops that have a price of less than 1200.
    """

    laptops_to_delete = Laptop.objects.filter(price__lt=1200)
    laptops_to_delete.delete()


def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    """
    Bulk creates one or more new instances of the model "ChessPlayer" class and saves them into the database.

    Parameters:
        args (List[ChessPlayer]): A list of ChessPlayer instances to be created
    Returns:
        None
    """
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    """
    Deletes all the chess players that have "no title".
    """
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won() -> None:
    """
    Changes the games won for the players with a "GM" title to 30.
    """
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost() -> None:
    """
    Changes the games lost for the players with "no title" to 25.
    """
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn() -> None:
    """
    Changes the games drawn for every player to 10.
    """
    ChessPlayer.objects.update(games_drawn=10)


def grand_chess_title_GM() -> None:
    """
    Changes the title to "GM" for every player with a rating greater than or equal to 2400.
    """
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM() -> None:
    """
    Changes the title to "IM" for every player with a rating between 2399 and 2300 (both inclusive).
    """
    ChessPlayer.objects.filter(rating__range=(2300, 2399)).update(title='IM')


def grand_chess_title_FM() -> None:
    """
    Changes the title to "FM" for every player with a rating between 2299 and 2200 (both inclusive).
    """
    ChessPlayer.objects.filter(rating__range=(2200, 2299)).update(title='FM')


def grand_chess_title_regular_player() -> None:
    """
    Changes the title to "regular player" for every player with a rating between 2199 and 0 (both inclusive).
    """
    ChessPlayer.objects.filter(rating__range=(0, 2199)).update(title='regular player')


def set_new_chefs() -> None:
    """
    Updates the name for every meal.
    • If the meal type is "Breakfast", update the chef's name to "Gordon Ramsay".
    • If the meal type is "Lunch", update the chef's name to "Julia Child".
    • If the meal type is "Dinner", update the chef's name to "Jamie Oliver".
    • If the meal type is "Snack", update the chef's name to "Thomas Keller".
    """
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value('Gordon Ramsay')),
            When(meal_type=MealTypeChoices.LUNCH, then=Value('Julia Child')),
            When(meal_type=MealTypeChoices.DINNER, then=Value('Jamie Oliver')),
            When(meal_type=MealTypeChoices.SNACK, then=Value('Thomas Keller')),
        )
    )


def set_new_preparation_times() -> None:
    """
    Updates the preparation time for every meal.
    • If the meal type is "Breakfast", update the preparation time to "10 minutes".
    • If the meal type is "Lunch", update the preparation time to "12 minutes".
    • If the meal type is "Dinner", update the preparation time to "15 minutes".
    • If the meal type is "Snack", update the preparation time to "5 minutes"
    """
    Meal.objects.update(
        preparation_time = Case(
            When(meal_type=MealTypeChoices.BREAKFAST, then=Value('10 minutes')),
            When(meal_type=MealTypeChoices.LUNCH, then=Value('12 minutes')),
            When(meal_type=MealTypeChoices.DINNER, then=Value('15 minutes')),
            When(meal_type=MealTypeChoices.SNACK, then=Value('5 minutes')),
        )
    )


def update_low_calorie_meals() -> None:
    """
    Changes the calories for the 'Breakfast' and 'Dinner' meals to 400.
    """
    Meal.objects.filter(
        meal_type__in=(MealTypeChoices.BREAKFAST,
                       MealTypeChoices.DINNER),
    ).update(
        calories=400,
    )


def update_high_calorie_meals() -> None:
    """
    Changes the calories for the 'Lunch' and 'Snack' meals to 700.
    """
    Meal.objects.filter(
        meal_type__in=(MealTypeChoices.LUNCH,
                       MealTypeChoices.SNACK),
    ).update(
        calories=700,
    )


def delete_lunch_and_snack_meals() -> None:
    """
    Deletes all 'Lunch' and 'Snack' meals.
    """
    Meal.objects.filter(
        meal_type__in=(MealTypeChoices.LUNCH,
                       MealTypeChoices.SNACK),
    ).delete()


def show_hard_dungeons() -> str:
    """
    Returns a string with only the "Hard" dungeons, ordered by location (descending)
    """
    hard_dungeons = Dungeon.objects.filter(difficulty=DungeonDifficultyChoices.HARD).order_by('-location')
    return '\n'.join(str(dungeon) for dungeon in hard_dungeons)


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    """
    Creates one or more new instances of the "Dungeon" class

    Parameters:
        args (List[Dungeon]): A list of Dungeon instances to be created
    """
    Dungeon.objects.bulk_create(args)


def update_dungeon_names() -> None:
    """
    Updates the name for all dungeons.
    • If the dungeon difficulty is "Easy", update the dungeon name to "The Erased Thombs".
    • If the dungeon difficulty is "Medium", update the dungeon name to "The Coral Labyrinth".
    • If the dungeon difficulty is "Hard", update the dungeon name to "The Lost Haunt".
    """
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value('The Erased Thombs')),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value('The Lost Haunt')),
        )
    )


def update_dungeon_bosses_health() -> None:
    """
    Changes the boss health to 500 for all dungeons except for the ones that have difficulty "Easy".
    """
    Dungeon.objects.exclude(
        difficulty=DungeonDifficultyChoices.EASY
    ).update(boss_health=500)


def update_dungeon_recommended_levels() -> None:
    """
    Updates the recommended level for all dungeons

    • If the dungeon difficulty is "Easy", update the recommended level to 25.
    • If the dungeon difficulty is "Medium", update the recommended level to 50.
    • If the dungeon difficulty is "Hard", update the recommended level to 75.
    """
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value(25)),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value(75)),
        )
    )


def update_dungeon_rewards() -> None:
    """
    Updates the difficulty for all dungeons.

    • If the dungeon boss's health is 500, update the dungeon reward to "1000 Gold".
    • If the dungeon's location starts with "E", update the reward to "New dungeon unlocked".
    • If the dungeon's location ends with "s", update the reward to "Dragonheart Amulet".
    """
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value('1000 Gold')),
            When(location__startswith='E', then=Value('New dungeon unlocked')),
            When(location__endswith='s', then=Value('Dragonheart Amulet')),
        )
    )


def set_new_locations() -> None:
    """
    Updates the location for all dungeons.

    • If the recommended level is 25, update the dungeon location to "Enchanted Maze".
    • If the recommended level is 50, update the dungeon location to "Grimstone Mines".
    • If the recommended level is 75, update the dungeon location to "Shadowed Abyss".
    """
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value('Enchanted Maze')),
            When(recommended_level=50, then=Value('Grimstone Mines')),
            When(recommended_level=75, then=Value('Shadowed Abyss')),
        )
    )


def show_workouts() -> str:
    """
    Retrieves and returns a string representation of workouts of specific types.

    This function filters the workouts to include only those of type 'Calisthenics' and 'CrossFit',
    and returns their string representations joined by newline characters.

    Returns:
        str: A string containing the string representations of the filtered workouts, each on a new line.
    """
    workouts = Workout.objects.filter(
        workout_type__in=(
            WorkoutTypeChoices.CALISTHENICS, 
            WorkoutTypeChoices.CROSSFIT,
        )
    )
    
    return '\n'.join(str(workout) for workout in workouts)


def get_high_difficulty_cardio_workouts() -> QuerySet:
    """
    Returns all workouts from type "Cardio" that have difficulty "High", ordered by the instructor.
    """
    return Workout.objects.filter(
        workout_type=WorkoutTypeChoices.CARDIO,
        difficulty='High'
    ).order_by('instructor')


def set_new_instructors():
    """
    Updates the instructors for all workouts.

    • If the workout type is "Cardio", update the instructor to "John Smith".
    • If the workout type is "Strength", update the instructor to "Michael Williams".
    • If the workout type is "Yoga", update the instructor to "Emily Johnson".
    • If the workout type is "CrossFit", update the instructor to "Sarah Davis".
    • If the workout type is "Calisthenics", update the instructor to "Chris Heria".
    """
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoices.CARDIO, then=Value('John Smith')),
            When(workout_type=WorkoutTypeChoices.STRENGTH, then=Value('Michael Williams')),
            When(workout_type=WorkoutTypeChoices.YOGA, then=Value('Emily Johnson')),
            When(workout_type=WorkoutTypeChoices.CROSSFIT, then=Value('Sarah Davis')),
            When(workout_type=WorkoutTypeChoices.CALISTHENICS, then=Value('Chris Heria')),
        )
    )


def set_new_duration_times() -> None:
    """
    Updates the duration of every workout.

    • If the instructor is "John Smith", update the duration time to "15 minutes".
    • If the instructor is "Sarah Davis", update the duration time to "30 minutes".
    • If the instructor is "Chris Heria", update the duration time to "45 minutes".
    • If the instructor is "Michael Williams", update the duration time to "1 hour".
    • If the instructor is "Emily Johnson", update the duration time to "1 hour and 30 minutes".
    """
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
        )
    )


def delete_workouts() -> None:
    """
    Deletes all workouts except the "Strength" and "Calisthenics".
    """
    Workout.objects.exclude(
        workout_type__in=(
            WorkoutTypeChoices.STRENGTH,
            WorkoutTypeChoices.CALISTHENICS,
        )
    ).delete()


# Run and print your queries

# artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
# artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)
#
# # Bulk saves the instances
# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())

# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
#
# # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)
#
# update_to_512_GB_storage()
# update_operation_systems()
#
# # Retrieve 2 laptops from the database
# asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
# lenovo_laptop = Laptop.objects.filter(brand__exact='Lenovo').get()
#
# print(asus_laptop.storage)
# print(lenovo_laptop.operation_system)

# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())

# meal1 = Meal.objects.create(
#     name="Pancakes",
#     meal_type="Breakfast",
#     preparation_time="20 minutes",
#     difficulty=3,
#     calories=350,
#     chef="Jane",
# )
#
# meal2 = Meal.objects.create(
#     name="Spaghetti Bolognese",
#     meal_type="Dinner",
#     preparation_time="45 minutes",
#     difficulty=4,
#     calories=550,
#     chef="Sarah",
# )
# # Test the set_new_chefs function
# set_new_chefs()
#
# # Test the set_new_preparation_times function
# set_new_preparation_times()
#
# # Refreshes the instances
# meal1.refresh_from_db()
# meal2.refresh_from_db()
#
# # Print the updated meal information
# print("Meal 1 Chef:", meal1.chef)
# print("Meal 1 Preparation Time:", meal1.preparation_time)
# print("Meal 2 Chef:", meal2.chef)
# print("Meal 2 Preparation Time:", meal2.preparation_time)

# Create two instances
# dungeon1 = Dungeon(
#     name="Dungeon 1",
#     boss_name="Boss 1",
#     boss_health=1000,
#     recommended_level=75,
#     reward="Gold",
#     location="Eternal Hell",
#     difficulty="Hard",
# )
#
# dungeon2 = Dungeon(
#     name="Dungeon 2",
#     boss_name="Boss 2",
#     boss_health=400,
#     recommended_level=25,
#     reward="Experience",
#     location="Crystal Caverns",
#     difficulty="Easy",
# )
#
# # Bulk save the instances
# bulk_create_dungeons([dungeon1, dungeon2])
#
# # Update boss's health
# update_dungeon_bosses_health()
#
# # Show hard dungeons
# hard_dungeons_info = show_hard_dungeons()
# print(hard_dungeons_info)
#
# # Change dungeon names based on difficulty
# update_dungeon_names()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].name)
# print(dungeons[1].name)
#
# # Change the dungeon rewards
# update_dungeon_rewards()
# dungeons = Dungeon.objects.order_by('boss_health')
# print(dungeons[0].reward)
# print(dungeons[1].reward)

# Create two Workout instances
# workout1 = Workout.objects.create(
#     name="Push-Ups",
#     workout_type="Calisthenics",
#     duration="10 minutes",
#     difficulty="Intermediate",
#     calories_burned=200,
#     instructor="Bob"
# )
#
# workout2 = Workout.objects.create(
#     name="Running",
#     workout_type="Cardio",
#     duration="30 minutes",
#     difficulty="High",
#     calories_burned=400,
#     instructor="Lilly"
# )
#
# # Run the functions
# print(show_workouts())
#
# high_difficulty_cardio_workouts = get_high_difficulty_cardio_workouts()
# for workout in high_difficulty_cardio_workouts:
#     print(f"{workout.name} by {workout.instructor}")
#
# set_new_instructors()
# for workout in Workout.objects.all():
#     print(f"Instructor: {workout.instructor}")
#
# set_new_duration_times()
# for workout in Workout.objects.all():
#     print(f"Duration: {workout.duration}")
