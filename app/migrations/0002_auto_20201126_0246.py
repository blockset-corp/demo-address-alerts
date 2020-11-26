# Generated by Django 3.1.3 on 2020-11-26 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='subscription_id',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='alert',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]