from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CS-Helper API",
        default_version="v1",
        description="API 문서",
        contact=openapi.Contact(name="test", email="test@test.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "v1/",
        include(
            (
                [
                    re_path(
                        r"^swagger(?P<format>\.json|\.yaml)$",
                        schema_view.without_ui(cache_timeout=0),
                        name="schema-json",
                    ),
                    re_path(
                        r"^swagger/$",
                        schema_view.with_ui("swagger", cache_timeout=0),
                        name="schema-swagger-ui",
                    ),
                    re_path(
                        r"^redoc/$",
                        schema_view.with_ui("redoc", cache_timeout=0),
                        name="schema-redoc",
                    ),
                    path("", include("api.v1.urls")),

                    path("", include("api.v1.user.urls")),
                    path("", include("api.v1.contract.urls")),
                    path("", include("api.v1.inquiry.urls")),
                ]
            )
        ),
    ),
]
