# Generated by Django 2.2.3 on 2020-07-24 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_order_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='statues',
            field=models.IntegerField(choices=[(1, '未付款'), (2, '已付款')], default=1),
        ),
    ]
