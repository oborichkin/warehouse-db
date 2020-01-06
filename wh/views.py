from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, permissions

from .serializers import *
from .models import *


class StorageLeftView(ListView):
    model = Product
    template_name = 'wh/storage_left.html'


class TransactionView(DetailView):
    model = Transaction
    template_name = 'wh/transaction.html'


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all().order_by('name')
    serializer_class = ProductTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('last_name')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class SalesViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('date')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
