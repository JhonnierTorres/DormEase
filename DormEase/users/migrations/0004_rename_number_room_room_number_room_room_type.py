# Generated by Django 5.2 on 2025-04-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_check_in_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='number',
            new_name='room_number',
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('quad', 'Quad')], default='double', max_length=10),
        ),
    ]
