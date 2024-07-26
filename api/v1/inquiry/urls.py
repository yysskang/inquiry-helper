from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.v1.inquiry.views import InquiryManagementViewSet, InquiryViewSet

router = DefaultRouter()
router.register(r'inquiry_management', InquiryManagementViewSet)
router.register(r'inquiry', InquiryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
