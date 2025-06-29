# Generated by Django 5.2 on 2025-06-27 06:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0003_clientprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DietPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('morning', models.TextField(blank=True)),
                ('afternoon', models.TextField(blank=True)),
                ('evening', models.TextField(blank=True)),
                ('night', models.TextField(blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='diet_plan', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_diet_plans', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
