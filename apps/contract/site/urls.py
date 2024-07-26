from django.urls import path
from apps.contract.site.views import ContractInfo

app_name = "contract"

urlpatterns = [
    path("", ContractInfo.as_view(), name="contract-info"),
]