from django.db import models
import decimal


class ProductType(models.Model):
    """Модель для типов товаров."""
    name = models.CharField(verbose_name='Название',
                            max_length=200, unique=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель конкретных для товаров."""
    name = models.CharField(verbose_name='Название',
                            max_length=200, unique=True)
    cost = models.DecimalField(
        verbose_name='Стоимость', max_digits=9, decimal_places=2)
    amount = models.PositiveIntegerField(verbose_name='Кол-во', default=0)
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
    total_spendings = models.PositiveIntegerField(
        verbose_name='Траты за всё время', default=0)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['last_name'])
        ]
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def calculate_discount(self):
        """Расчитывает скидку для покупателя"""
        if self.total_spendings < 5000:
            return 1
        if self.total_spendings < 10000:
            return 0.95
        return 0.90


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
    delivery_cost = models.DecimalField(
        verbose_name='Стоимость доставки', max_digits=9, decimal_places=2, default=0)
    date = models.DateTimeField('Дата', auto_now_add=True)
    total_cost = models.DecimalField(
        'Стоимость', max_digits=9, decimal_places=2, default=0)
    certificate = models.OneToOneField(
        to='Sales',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={'product__type__name': 'Сертификат'}
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f"{self.product} x{self.amount}"

    def save(self, *args, **kwargs):
        self.total_cost = (self.product.cost * self.amount) * \
            decimal.Decimal(self.buyer.calculate_discount()) + \
            self.delivery_cost
        if self.certificate:
            self.total_cost = max(0, self.total_cost -
                                  self.certificate.total_cost)
        self.buyer.total_spendings += self.total_cost
        self.buyer.save()
        self.product.amount -= self.amount
        self.product.save()
        super().save(*args, **kwargs)
