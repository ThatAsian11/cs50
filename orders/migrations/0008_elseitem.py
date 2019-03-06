# Generated by Django 2.0.3 on 2019-02-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_delete_elseitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('small', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('large', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('base', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
    ]
