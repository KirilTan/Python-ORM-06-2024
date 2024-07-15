from django.db import models

from main_app.choices import StudentEnrollmentGradeChoices


# Create your models here.

class Lecturer(models.Model):
    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        text = f'{self.first_name} {self.last_name}'
        return text


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
    )

    code = models.CharField(
        max_length=10,
    )

    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        text = self.name
        return text


class Student(models.Model):
    student_id = models.CharField(
        max_length=10,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
    )

    birth_date = models.DateField()

    email = models.EmailField(
        unique=True,
    )

    subjects = models.ManyToManyField(
        to=Subject,
        through='StudentEnrollment',
    )


class StudentEnrollment(models.Model):
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
    )

    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
    )

    enrollment_date = models.DateField(
        auto_now_add=True,
    )

    grade = models.CharField(
        max_length=1,
        choices=StudentEnrollmentGradeChoices.choices
    )

    def __str__(self):
        text = f'{self.student} enrolled in {self.subject}'
        return text