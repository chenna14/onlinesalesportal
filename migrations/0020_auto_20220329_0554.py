# Generated by Django 2.2.5 on 2022-03-29 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20220329_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Pending', 'Pending')], max_length=200, null=True),
        ),
    ]