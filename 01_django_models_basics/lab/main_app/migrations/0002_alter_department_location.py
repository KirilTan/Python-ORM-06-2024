# Generated by Django 5.0.4 on 2024-06-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='location',
            field=models.CharField(choices=[('Sofia', 'Sofia'), ('Plovdiv', 'Plovdiv'), ('Varna', 'Varna'), ('Burgas', 'Burgas')], max_length=50),
        ),
    ]
