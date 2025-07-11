# Generated by Django 5.2.1 on 2025-05-28 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название курса', max_length=100, verbose_name='Название курса')),
                ('preview', models.ImageField(blank=True, help_text='Укажите картинку курса', null=True, upload_to='lms/preview/course/', verbose_name='Картинка')),
                ('description', models.TextField(blank=True, help_text='Введите описание курса', null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Введите название урока', max_length=100, verbose_name='Название урока')),
                ('description', models.TextField(blank=True, help_text='Введите описание урока', null=True, verbose_name='Описание')),
                ('preview', models.ImageField(blank=True, help_text='Укажите картинку урока', null=True, upload_to='lms/preview/lesson/', verbose_name='Картинка')),
                ('video_url', models.URLField(blank=True, help_text='Вставьте ссылку на видео', null=True, verbose_name='Ссылка на видео')),
                ('course', models.ForeignKey(help_text='Выберите курс, к которому относится урок', on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lms.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]
