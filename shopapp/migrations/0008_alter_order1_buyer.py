# Generated by Django 4.1.4 on 2023-03-24 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0007_alter_order1_buyer_alter_order1_delivery_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order1',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopapp.profile'),
        ),
    ]
