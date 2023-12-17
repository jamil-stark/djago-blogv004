# Generated by Django 4.2.1 on 2023-12-16 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("myblogAppV3", "0003_alter_blogmodel_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogmodel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="blog_posts_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]