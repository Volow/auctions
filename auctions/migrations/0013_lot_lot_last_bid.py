# Generated by Django 4.0.3 on 2022-04-30 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='lot_last_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
