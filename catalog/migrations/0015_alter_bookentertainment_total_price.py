# Generated by Django 4.2.8 on 2024-02-13 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_bookentertainment_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookentertainment',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]