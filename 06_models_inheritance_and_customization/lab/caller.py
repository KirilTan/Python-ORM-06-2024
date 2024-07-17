import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Animal, Mammal, Bird, Reptile


# Create queries within functions
Animal.objects.create(name="Nemo", species="Clownfish", birth_date="2019-04-10", sound="Bubbles")
Mammal.objects.create(name="Fluffy", species="Orangutan", birth_date="2018-02-10", sound="Chomps", fur_color="Reddish-brown")
Bird.objects.create(name="Robby", species="American Robin", birth_date="2021-03-20", sound="Chirp", wing_span=28.50)
Reptile.objects.create(name="Python", species="Ball Python", birth_date="2019-07-01", sound="Hiss", scale_type="Smooth")

animals = Animal.objects.all()
for a in animals:
    print(f"{a.name}: {a.species}.")
