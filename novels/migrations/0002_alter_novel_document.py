# Generated by Django 5.0.3 on 2024-03-30 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("novels", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="novel",
            name="document",
            field=models.FileField(
                blank=True,
                help_text="Upload PDF document",
                null=True,
                upload_to="novels/",
            ),
        ),
    ]
