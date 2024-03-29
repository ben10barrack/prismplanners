# Generated by Django 4.2.8 on 2024-02-12 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0010_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCatering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('num_guests', models.PositiveIntegerField()),
                ('contact_info', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('R', 'Rejected')], default='P', max_length=1)),
                ('catering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.catering')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
