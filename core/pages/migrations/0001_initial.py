# Generated by Django 4.1.7 on 2023-03-29 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParseResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=0, verbose_name='Порядковый номер')),
                ('order_id', models.PositiveIntegerField(default=0, verbose_name='Заказ №')),
                ('price', models.FloatField(default=0, verbose_name='Cтоимость,$')),
                ('delivery_time', models.DateField(verbose_name='Срок поставки')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Время получения данных')),
            ],
        ),
    ]
