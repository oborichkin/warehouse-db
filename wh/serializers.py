from rest_framework import serializers

from .models import *


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductType
        fields = ('id', 'name', )


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'cost', 'units', 'type')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        depth = 1
        fields = ('id', 'date', 'buyer', 'items', 'delivery_cost', 'total_cost', 'certificate')