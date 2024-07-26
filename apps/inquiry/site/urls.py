from django.urls import path
from apps.inquiry.site.views import InquiryList, InquiryDetail, InquiryManagement, InquiryService

app_name = "inquiry"

urlpatterns = [
    path("list/", InquiryList.as_view(), name="inquiry-list"),
    path("detail/<int:pk>/", InquiryDetail.as_view(), name="inquiry-detail"),
    path("management/", InquiryManagement.as_view(), name="inquiry-management"),
    path("service/<str:key>/", InquiryService.as_view(), name="inquiry-service"),
]