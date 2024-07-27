# caller.py

from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


def get_directors(search_name: str = None, search_nationality: str = None) -> str:
    """
    This function retrieves a list of directors based on the provided search criteria.

    Parameters:
        search_name (str, optional): The name of the director to search for. 
                                     If not provided, all directors will be returned.
        search_nationality (str, optional): The nationality of the director to search for. 
                                            If not provided, all directors will be returned.

    Returns:
        str: A formatted string containing the details of the retrieved directors. 
             If no directors are found, an empty string is returned.
    """
    if search_name is None and search_nationality is None:
        return ""

    query = Q()
    if search_name is not None:
        query &= Q(full_name__icontains=search_name)
    if search_nationality is not None:
        query &= Q(nationality__icontains=search_nationality)

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors.exists():
        return ""

    result = []
    for director in directors:
        result.append(f"Director: {director.full_name}, "
                      f"nationality: {director.nationality}, "
                      f"experience: {director.years_of_experience}")

    return "\n".join(result)


def get_top_director() -> str:
    """
    Retrieves the director with the highest number of movies in the database.

    Returns:
        str: A formatted string containing the name of the top director and the number of movies they have directed.
             If no directors are found in the database, an empty string is returned.
    """
    top_director = Director.objects.get_directors_by_movies_count().first()

    if not top_director:
        return ''

    return f"Top Director: {top_director.full_name}, movies: {top_director.movie_count}."


def get_top_actor() -> str:
    """
    Retrieves the actor with the highest number of main character appearances in the database.

    The function first annotates each actor with the count of their main character appearances in movies.
    It then orders the actors by the count in descending order and by their full name in ascending order.
    If no actors are found in the database, an empty string is returned.

    If an actor is found, the function retrieves all the movies in which the actor has a main character.
    If no movies are found for the actor, an empty string is returned.

    The function then calculates the average rating of the actor's movies.
    If no rating is found, the average rating is set to 0.0.

    Finally, the function constructs and returns a formatted string containing the actor's name,
    the titles of the movies in which they have a main character, and the average rating of their movies.

    Returns:
        str: A formatted string containing the top actor's name, the titles of the movies in which they have a main character,
             and the average rating of their movies. If no actors or movies are found, an empty string is returned.
    """
    actors = Actor.objects.annotate(
        starring_count=Count('main_character_in_movies')
    ).order_by('-starring_count', 'full_name')

    if not actors.exists():
        return ""

    top_actor = actors.first()
    movies = top_actor.main_character_in_movies.all()

    if not movies.exists():
        return ""

    avg_rating = movies.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0
    movie_titles = ", ".join(movie.title for movie in movies)

    return f'Top Actor: {top_actor.full_name}, starring in movies: {movie_titles}, movies average rating: {avg_rating:.1f}'


def get_actors_by_movies_count():
    """
    Retrieves the top three actors with the highest number of appearances in movies.

    The function first retrieves all actors using the `top_three_actors` custom manager method.
    It then checks if there are any movies and actors in the database.
    If either condition is not met, an empty string is returned.

    If actors are found, the function iterates over each actor,
    appending a formatted string to the `result` list.
    The string includes the actor's full name and the number of movies they have appeared in.

    Finally, the function joins the `result` list into a single string using newline characters,
    and returns the formatted string.

    Returns:
        str: A formatted string containing the top three actors' names and the number of movies they have appeared in.
             If no actors or movies are found, an empty string is returned.
    """
    actors = Actor.objects.top_three_actors()

    if not Movie.objects.all() or not actors:
        return ''

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.appearance_count} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie() -> str:
    """
    Retrieves the top-rated awarded movie from the database.

    The function filters movies that are awarded and ordered by rating in descending order,
    then by title in ascending order. It retrieves the first movie from the filtered queryset.

    If no awarded movies are found, the function returns an empty string.

    If a top-rated awarded movie is found, the function extracts the starring actor's name,
    if available, or assigns 'N/A' if no starring actor is found.
    It also retrieves the full names of all actors in the movie, ordered by their names.

    The function then constructs and returns a formatted string containing the movie's title,
    rating, starring actor's name, and the full names of all actors in the movie.

    Returns:
        str: A formatted string containing the movie's title, rating, starring actor's name,
             and the full names of all actors in the movie.
             If no awarded movies are found, an empty string is returned.
    """
    top_movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if not top_movie:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'
    cast = ', '.join(actor.full_name for actor in top_movie.actors.order_by('full_name'))

    return (f"Top rated awarded movie: {top_movie.title}, "
            f"rating: {top_movie.rating:.1f}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")


def increase_rating() -> str:
    """
    Increases the rating of classic movies by 0.1.

    This function retrieves all classic movies from the database with a rating less than 10.0.
    It then updates the rating of each classic movie by adding 0.1 to its current rating.
    The function returns a string indicating the number of movies whose ratings have been increased.

    Returns:
        str: A string indicating the number of movies whose ratings have been increased.
             If no ratings have been increased, the string "No ratings increased." is returned.
    """
    classic_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)
    updated_count = classic_movies.update(rating=F('rating') + 0.1)

    if updated_count == 0:
        return "No ratings increased."

    return f"Rating increased for {updated_count} movies."
