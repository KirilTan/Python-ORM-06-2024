from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from exception import RelationException
from helpers import session_decorator
from models import Recipe, Chef
from seed import recipes

engine = create_engine("postgresql+psycopg2://postgres:admin@localhost/sql_alchemy_db")
Session = sessionmaker(bind=engine)

session = Session()


@session_decorator(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    """
    Creates a new recipe and adds it to the database.

    Args:
        name (str): The name of the recipe.
        ingredients (str): A string containing the ingredients of the recipe.
        instructions (str): A string containing the instructions for the recipe.

    Returns:
        None
    """
    new_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )

    session.add(new_recipe)


@session_decorator(session)
def update_recipe_by_name(name: str, new_name: str, new_ingredients: str, new_instructions: str) -> int:
    """
    Updates an existing recipe's name, ingredients, and instructions in the database.

    Args:
        name (str): The current name of the recipe to be updated.
        new_name (str): The new name for the recipe.
        new_ingredients (str): The new ingredients for the recipe.
        new_instructions (str): The new instructions for the recipe.

    Returns:
        int: The number of records that were changed.
    """
    records_changed: int = (
        session.query(Recipe)
        .filter_by(name=name)
        .update({
            Recipe.name: new_name,
            Recipe.ingredients: new_ingredients,
            Recipe.instructions: new_instructions
        })
    )

    return records_changed


@session_decorator(session)
def delete_recipe_by_name(name: str) -> int:
    """
    Deletes a recipe from the database by its name.

    Args:
        name (str): The name of the recipe to be deleted.

    Returns:
        int: The number of records that were deleted.
    """
    records_changed: int = (
        session.query(Recipe)
        .filter_by(name=name)
        .delete()
    )

    return records_changed


@session_decorator(session, autoclose_session=False)
def get_recipes_by_ingredient(ingredient_name: str) -> List:
    """
    Retrieves a list of recipes that contain a specific ingredient.

    Args:
        ingredient_name (str): The name of the ingredient to search for in the recipes.

    Returns:
        List: A list of Recipe objects that contain the specified ingredient.
    """
    recipes_with_ingredient = (
        session.query(Recipe)
        .filter(Recipe.ingredients.ilike(f"%{ingredient_name}%"))
        .all()
    )

    return recipes_with_ingredient


@session_decorator(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str) -> None:
    """
    Swaps the ingredients between two recipes identified by their names.

    Args:
        first_recipe_name (str): The name of the first recipe.
        second_recipe_name (str): The name of the second recipe.

    Returns:
        None
    """
    first_recipe = (
        session.query(Recipe)
        .filter_by(name=first_recipe_name)
        .with_for_update()
        .one()
    )

    second_recipe = (
        session.query(Recipe)
        .filter_by(name=second_recipe_name)
        .with_for_update()
        .one()
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@session_decorator(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    """
    Relates a recipe with a chef by their names.

    This function associates a recipe with a chef in the database. If the recipe
    already has a related chef, it raises a RelationException.

    Args:
        recipe_name (str): The name of the recipe to be related to a chef.
        chef_name (str): The name of the chef to be related to the recipe.

    Returns:
        str: A message indicating the successful relation of the recipe with the chef.
    """
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()

    if recipe and recipe.chef:
        raise RelationException(f"Recipe: {recipe_name} already has a related chef")

    chef = session.query(Chef).filter_by(name=chef_name).first()

    recipe.chef = chef

    return f"Related recipe {recipe_name} with chef {chef_name}"


def get_recipes_with_chef() -> str:
    """
    Retrieves a list of recipes along with their associated chefs.

    This function queries the database to get the names of recipes and their related chefs,
    then formats the results into a string.

    Returns:
        str: A formatted string listing each recipe and its associated chef.
    """
    recipes_with_chef = (
        session.query(Recipe.name, Chef.name.label("chef_name"))
        .join(Chef, Recipe.chef)
        .all()
    )

    return "\n".join(
        f"Recipe: {recipe_name} made by chef: {chef_name}"
        for recipe_name, chef_name in recipes_with_chef
    )
