# Generated by Django 3.0.2 on 2020-01-06 20:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wh', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='certificate',
            field=models.OneToOneField(blank=True, limit_choices_to={'product__type__name': 'Сертификат'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usage', to='wh.SalesItem'),
        ),
    ]