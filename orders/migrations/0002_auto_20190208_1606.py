# Generated by Django 2.0.3 on 2019-02-08 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('options', models.CharField(choices=[('Y', 'Yes'), ('N', 'No'), ('C', 'Cheese-only')], default='N', max_length=1)),
                ('size', models.CharField(blank=True, choices=[('S', 'Small'), ('L', 'Large'), ('', '')], max_length=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('number_of_toppings', models.SmallIntegerField(choices=[(0, 'No extra toppings'), (1, '1 topping'), (2, '2 toppings'), (3, '3 toppings'), (5, 'Special')], default=0)),
                ('crust', models.CharField(blank=True, choices=[('S', 'Sicilian'), ('R', 'Italian'), ('', '')], default='', max_length=1)),
            ],
            options={
                'ordering': ('type_new', 'name', 'size', 'number_of_toppings'),
            },
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('valid_for', models.CharField(choices=[('P', 'Pizza Only'), ('S', 'Subs Only'), ('B', 'Both Pizza and Subs')], max_length=1)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20)),
                ('order_on_menu', models.IntegerField(default=0)),
                ('image_name', models.CharField(max_length=32, null=True)),
            ],
            options={
                'ordering': ('order_on_menu',),
            },
        ),
        migrations.AddField(
            model_name='menuitem',
            name='type_new',
            field=models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Type'),
        ),
    ]