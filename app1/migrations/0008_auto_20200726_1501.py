# Generated by Django 2.2.3 on 2020-07-26 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20200726_1340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='statues',
            new_name='status',
        ),
    ]