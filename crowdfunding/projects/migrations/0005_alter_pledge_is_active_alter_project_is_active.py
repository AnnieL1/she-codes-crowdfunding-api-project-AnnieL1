# Generated by Django 4.1.5 on 2023-01-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_pledge_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pledge',
            name='is_active',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(),
        ),
    ]
