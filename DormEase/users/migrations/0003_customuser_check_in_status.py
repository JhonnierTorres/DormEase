# Generated by Django 5.1.3 on 2025-04-07 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_move_in_date_customuser_student_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='check_in_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('checked_in', 'Checked In')], default='pending', max_length=20),
        ),
    ]
