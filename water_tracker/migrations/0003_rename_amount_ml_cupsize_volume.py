# Generated by Django 4.2.13 on 2024-06-04 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('water_tracker', '0002_cupsize_alter_wateringested_amount_ml'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cupsize',
            old_name='amount_ml',
            new_name='volume',
        ),
    ]
