from django.db import models


# №	заказ №	стоимость,$	срок поставки
# Create your models here.
class ParseResult(models.Model):
    number = models.PositiveIntegerField(default=0,
                                         verbose_name='Порядковый номер'
                                         )

    order_id = models.PositiveIntegerField(default=0,
                                           verbose_name='Заказ №',
                                           )

    price = models.FloatField(default=0,
                              verbose_name='Cтоимость,$',
                              )

    delivery_time = models.DateField(verbose_name='Срок поставки',
                                    )

    created_at = models.DateTimeField(verbose_name='Время получения данных',
                                      auto_now=True,
                                      )
