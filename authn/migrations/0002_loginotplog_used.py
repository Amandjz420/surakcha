# Generated by Django 3.0.7 on 2020-06-04 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authn', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginotplog',
            name='used',
            field=models.BooleanField(default=False),
        ),
    ]