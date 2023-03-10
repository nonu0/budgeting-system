# Generated by Django 4.1.5 on 2023-01-24 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=10)),
                ('last_name', models.CharField(max_length=10)),
                ('username', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'female')])),
                ('phone_no', models.IntegerField()),
                ('code', models.IntegerField()),
                ('address', models.IntegerField()),
                ('county', models.CharField(max_length=20)),
                ('town', models.CharField(max_length=20)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default='default.png', null=True, upload_to='media')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('source', models.CharField(max_length=30)),
                ('planned_amount', models.IntegerField()),
                ('actual_amount', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('name_of_expense', models.CharField(max_length=10)),
                ('category', models.IntegerField(choices=[(1, 'HouseHold'), (2, 'Food'), (3, 'Transportation'), (4, 'Personal'), (5, 'Subscriptions'), (6, 'Savings'), (7, 'Medical')])),
                ('planned_amount', models.IntegerField()),
                ('actual_amount', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_to', models.CharField(max_length=30)),
                ('planned_amount', models.IntegerField()),
                ('actual_amount', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.owner')),
            ],
        ),
    ]
