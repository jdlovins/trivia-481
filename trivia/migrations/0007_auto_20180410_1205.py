# Generated by Django 2.0.1 on 2018-04-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia', '0006_auto_20180408_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[('Sports', 'sports'), ('School', 'school'), ('History', 'history'), ('Dank Memes', 'dank memes'), ('Blumisms', 'blumisms'), ('Computers', 'computers'), ('Cars', 'cars'), ('Famous People', 'famous people'), ('Sciences', 'sciences'), ('Entertainment', 'entertainment'), ('Arts', 'arts')], max_length=20),
        ),
    ]