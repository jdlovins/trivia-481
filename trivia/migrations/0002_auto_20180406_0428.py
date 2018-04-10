# Generated by Django 2.0.1 on 2018-04-06 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittedanswer',
            name='answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trivia.Answer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submittedanswer',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trivia.GameUser'),
            preserve_default=False,
        ),
    ]