# Generated by Django 3.0.5 on 2020-04-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hallOfFameClient', '0004_auto_20200427_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]