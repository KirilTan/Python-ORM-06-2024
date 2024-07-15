import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Lecturer, Subject, Lecturer, LecturerProfile


# Create queries within functions
# lecturer1 = Lecturer.objects.create(first_name="John", last_name="Doe")
# lecturer2 = Lecturer.objects.create(first_name="Jane", last_name="Smith")
# Subject.objects.create(name="Mathematics", code="MATH101", lecturer=lecturer1)
# Subject.objects.create(name="History", code="HIST101", lecturer=lecturer2)
# Subject.objects.create(name="Physics", code="PHYS101", lecturer=lecturer1)
# math_subject = Subject.objects.get(name="Mathematics")
# math_lecturer = math_subject.lecturer
# print(f"The lecturer for Mathematics is {math_lecturer}.")
#
# history_subject = Subject.objects.get(name="History")
# history_lecturer = history_subject.lecturer
# print(f"The lecturer for History is {history_lecturer}.")
#
# physics_subject = Subject.objects.get(name="Physics")
# physics_lecturer = physics_subject.lecturer
# print(f"The lecturer for Physics is {physics_lecturer}.")

# Keep the data from the previous exercises, so you can reuse it

# lecturer = Lecturer.objects.get(first_name='John', last_name="Doe")
# lecturer_profile = LecturerProfile.objects.create(lecturer=lecturer, email="john.doe@university.lecturers.com", bio="A skilled and passionate math lecturer", office_location="Sofia, Al. Stamobolyiski Str, Faculty of Mathematics and Computer Science, Room 101")
#
# lecturer_profile_from_db = LecturerProfile.objects.get(email='john.doe@university.lecturers.com')
#
# print(f"{lecturer_profile_from_db.lecturer.first_name} {lecturer_profile_from_db.lecturer.last_name} has a profile.")
