# Generated by Django 4.2.3 on 2023-07-31 11:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("direct_messages", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="room",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="direct_messages.chattingroom"),
        ),
        migrations.AlterField(
            model_name="message",
            name="user",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="messages", to=settings.AUTH_USER_MODEL),
        ),
    ]