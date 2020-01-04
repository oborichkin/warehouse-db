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
        fields = ('id', 'first_name', 'last_name', 'status')


class SalesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sales
        fields = ('id', 'date', 'product', 'buyer', 'amount', 'delivery_cost', 'total_cost', 'certificate')