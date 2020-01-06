# Generated by Django 3.0.2 on 2020-01-06 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=128, verbose_name='Фамилия')),
                ('total_spendings', models.PositiveIntegerField(default=0, verbose_name='Траты за всё время')),
            ],
            options={
                'verbose_name': 'Покупатель',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Стоимость')),
                ('units', models.CharField(choices=[('M', 'метр'), ('CM', 'сантиметр'), ('SM', 'квадратный метр'), ('QM', 'кубический метр')], max_length=2, verbose_name='Ед. Измерения')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип продукта',
                'verbose_name_plural': 'Типы продуктов',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='кол-во')),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Стоимость доставки')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Стоимость')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchases', related_query_name='purchase', to='wh.Customer')),
                ('certificate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wh.Sales')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sales', related_query_name='transaction', to='wh.Product')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.AddIndex(
            model_name='producttype',
            index=models.Index(fields=['name'], name='wh_productt_name_81ad03_idx'),
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', related_query_name='product', to='wh.ProductType'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['first_name', 'last_name'], name='wh_customer_first_n_41eb34_idx'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name'], name='wh_customer_last_na_445c72_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='wh_product_name_c1b2fc_idx'),
        ),
    ]