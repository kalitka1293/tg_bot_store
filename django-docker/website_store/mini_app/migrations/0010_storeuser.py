# Generated by Django 5.2 on 2025-05-09 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_app', '0009_remove_basket_product_delete_order_delete_basket'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(auto_created=True)),
                ('created', models.DateTimeField(auto_created=True)),
                ('telegram_id', models.IntegerField()),
                ('telegram_username', models.CharField()),
                ('telegram_first_name', models.CharField(null=True)),
                ('telegram_last_name', models.CharField(null=True)),
            ],
        ),
    ]
