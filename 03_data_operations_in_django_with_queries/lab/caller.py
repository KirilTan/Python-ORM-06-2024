import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date=date(1995, 5, 15),
        email='john.doe@university.com'
    )

    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        birth_date=None,
        email='jane.smith@university.com'
    )
    student.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date=date(1998, 2, 10),
        email='alice.johnson@university.com'
    )

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date=date(1996, 11, 25),
        email='bob.wilson@university.com'
    )


# Run and print your queries
add_students()
print(Student.objects.all())
