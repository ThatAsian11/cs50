# Generated by Django 2.0.3 on 2019-02-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['order_id']},
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
    ]