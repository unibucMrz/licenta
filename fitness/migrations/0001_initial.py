# Generated by Django 3.1.7 on 2021-05-17 08:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fitness.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DurationField()),
                ('date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the training day.', max_length=1000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, help_text='Enter a brief description of the exercise.', max_length=1000, null=True)),
                ('tutorial', models.FileField(blank=True, null=True, upload_to='tutorials/')),
                ('priority', models.IntegerField(choices=[(1, 'Start'), (2, 'Middle'), (3, 'End')])),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, validators=[fitness.validators.validate_trainer])),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='ExerciseInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.day')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitness.exercise')),
            ],
            options={
                'ordering': ['exercise', 'day'],
            },
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('repetitions', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='WeightAtDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(350)])),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user', 'date'],
            },
        ),
        migrations.CreateModel(
            name='TrainerRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_request', to=settings.AUTH_USER_MODEL)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SetPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done_set', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='done_set', to='fitness.set')),
                ('exercise', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='fitness.exerciseinstance')),
                ('given_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='given_set', to='fitness.set')),
            ],
        ),
    ]