# Generated by Django 4.2.8 on 2024-02-03 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_guest_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='venue_images/'),
        ),
    ]
