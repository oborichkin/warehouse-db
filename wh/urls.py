from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'types', views.ProductTypeViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'sales', views.SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api', include('rest_framework.urls', namespace='rest_framework')),
    path('storage', views.StorageLeftView.as_view()),
    path('transaction/<int:pk>', views.TransactionView.as_view())
]