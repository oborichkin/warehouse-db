from django.db import models
from django.db.models import Sum
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
                                 ('QT', 'Шт.'),
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
        
    def decrease_amount(self, amount):
        self.amount -= amount
        self.save()


class Customer(models.Model):
    """Модель для покупаетелей."""
    first_name = models.CharField(verbose_name='Имя', max_length=128)
    last_name = models.CharField(verbose_name='Фамилия', max_length=128)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['last_name'])
        ]
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_spendings(self):
        return Transaction.objects.filter(buyer=self).aggregate(Sum('total_cost'))['total_cost__sum']

    def calculate_discount(self):
        """Расчитывает скидку для покупателя"""
        if self.total_spendings < 5000:
            return 1
        if self.total_spendings < 10000:
            return 0.95
        return 0.90


class SalesItem(models.Model):
    """Модель для позиции в чеке"""
    product = models.ForeignKey(
        to='Product',
        on_delete=models.PROTECT
    )
    amount = models.PositiveIntegerField(verbose_name='кол-во')
    transaction = models.ForeignKey(
        to="Transaction",
        on_delete=models.CASCADE,
        related_name='items',
        related_query_name='items'
    )
    
    class Meta:
        verbose_name = 'Позиция чека'
        verbose_name_plural = 'Позиции чека'

class Transaction(models.Model):
    """Модель для чека."""
    buyer = models.ForeignKey(
        to='Customer',
        on_delete=models.PROTECT,
        related_name='purchases',
        related_query_name='purchase'
    )
    delivery_cost = models.DecimalField(
        verbose_name='Стоимость доставки', max_digits=9, decimal_places=2, default=0)
    date = models.DateTimeField('Дата', auto_now_add=True)
    total_cost = models.DecimalField('Стоимость', max_digits=9, decimal_places=2, default=0)
    certificate = models.OneToOneField(
        to='SalesItem',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={'product__type__name': 'Сертификат'},
        related_name='usage'
    )

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f"<{self.date}>"

    @property
    def get_discount_amount(self):
        return f"{self.total_cost - self.total_cost * decimal.Decimal(self.buyer.calculate_discount()):.2f}"

    def save(self, *args, **kwargs):
        self.total_cost = 0
        for item in self.items.all():
            self.total_cost += item.product.cost * item.amount
            item.product.decrease_amount(item.amount)
        self.total_cost *= decimal.Decimal(self.buyer.calculate_discount())
        self.total_cost += self.delivery_cost
        if self.certificate:
            self.total_cost = max(0, self.total_cost -
                                  self.certificate.product.cost)
        super().save(*args, **kwargs)
