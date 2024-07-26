from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.contract.views import ContractViewSet

router = DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
]