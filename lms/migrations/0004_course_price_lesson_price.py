# Generated by Django 5.2.1 on 2025-06-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0003_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=0, help_text='Введите цену курса', verbose_name='Цена курса'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.PositiveIntegerField(default=0, help_text='Введите цену урока', verbose_name='Цена урока'),
        ),
    ]
