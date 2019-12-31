from django.db import models


class ProductType(models.Model):
    """Модель для типов товаров."""
    name = models.CharField(verbose_name='Название', max_length=200)

    def __str__(self):
        return name


class Product(models.Model):
    """Модель конкретных для товаров."""
    name = models.CharField(verbose_name='Название', max_length=200)
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=9, decimal_places=2)
    units = models.CharField(verbose_name='Ед. Измерения',
        choices=(
            ('M', 'метр'),
            ('CM', 'сантиметр'),
            ('SM', 'квадратный метр'),
            ('QM', 'кубический метр')
        )
    )
    type = models.ForeignKey('ProductType')

    def __str__(self):
        return f"{self.name}"


class Customer(models.Model):
    """Модель для покупаетелей."""
    first_name = models.CharField(verbose_name='Имя', max_length=128)
    last_name = models.CharField(verbose_name='Фамилия', max_length=128)
    status = models.CharField(verbose_name='Статус',
        choices=(
            ('B', 'Бронза'),
            ('S', 'Серебро'),
            ('G', 'Золото'),
            ('P', 'Платина')
        )
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.status}]"


class Sales(models.Model):
    """Модель для продаж."""
    product = model.ForeignKey('Product')
    buyer = models.ForeignKey('Customer')
    amount = models.PositiveIntegerField(verbose_name='кол-во')
    delivery_cost = models.DecimalField(verbose_name='Стоимость доставки', max_digits=9, decimal_places=2)
    date = models.DateTimeField('Дата', auto_now_add=True)
    total_cost = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)
    certificate = models.ForeignKey('Sales')

    def __str__(self):
        return f"{self.product} x{self.amount}"
