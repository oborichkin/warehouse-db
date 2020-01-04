from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .serializers import *
from .models import *


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all().order_by('name')
    serializer_class = ProductTypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('last_name')
    serializer_class = CustomerSerializer


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Sales.objects.all().order_by('date')
    serializer_class = SalesSerializer
