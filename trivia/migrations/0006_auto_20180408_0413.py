# Generated by Django 2.0.1 on 2018-04-08 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0005_gameuser_points'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='started',
        ),
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.CharField(choices=[('PRE GAME', 'PRE GAME'), ('STARTED', 'STARTED'), ('NONE', 'NONE')], default='NONE', max_length=15),
        ),
    ]
