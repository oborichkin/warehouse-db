from django.db import models


class ProductType(models.Model):
    """Модель для типов товаров."""
    name = models.CharField(verbose_name='Название', max_length=200, unique=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель конкретных для товаров."""
    name = models.CharField(verbose_name='Название', max_length=200, unique=True)
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=9, decimal_places=2)
    units = models.CharField(verbose_name='Ед. Измерения', max_length=2,
        choices=(
            ('M', 'метр'),
            ('CM', 'сантиметр'),
            ('SM', 'квадратный метр'),
            ('QM', 'кубический метр')
        )
    )
    type = models.ForeignKey(
        to='ProductType',
        on_delete=models.PROTECT,
        related_name='products',
        related_query_name='product'
    )

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    """Модель для покупаетелей."""
    first_name = models.CharField(verbose_name='Имя', max_length=128)
    last_name = models.CharField(verbose_name='Фамилия', max_length=128)
    status = models.CharField(verbose_name='Статус', max_length=1,
        choices=(
            ('B', 'Бронза'),
            ('S', 'Серебро'),
            ('G', 'Золото'),
            ('P', 'Платина')
        )
    )

    class Meta:
        indexes = [models.Index(fields=['first_name', 'last_name'])]
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.status}]"


class Sales(models.Model):
    """Модель для продаж."""
    product = models.ForeignKey(
        to='Product',
        on_delete=models.PROTECT,
        related_name='sales',
        related_query_name='transaction'
    )
    buyer = models.ForeignKey(
        to='Customer',
        on_delete=models.PROTECT,
        related_name='purchases',
        related_query_name='purchase'
    )
    amount = models.PositiveIntegerField(verbose_name='кол-во')
    delivery_cost = models.DecimalField(verbose_name='Стоимость доставки', max_digits=9, decimal_places=2)
    date = models.DateTimeField('Дата', auto_now_add=True)
    total_cost = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)
    certificate = models.ForeignKey(
        to='Sales',
        on_delete=models.PROTECT,
        blank=True
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f"{self.product} x{self.amount}"
