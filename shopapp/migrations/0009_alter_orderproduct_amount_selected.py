# Generated by Django 4.1.4 on 2023-03-24 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0008_alter_order1_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='amount_selected',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
