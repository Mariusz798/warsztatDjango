# Generated by Django 3.2 on 2021-04-17 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_alter_reservationmodel_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationmodel',
            old_name='room_id',
            new_name='room',
        ),
    ]
