# Generated by Django 2.2.3 on 2020-07-26 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_auto_20200726_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, '未付款'), (2, '已付款')], default=1),
        ),
    ]