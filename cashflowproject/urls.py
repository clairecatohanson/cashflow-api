from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from cashflowapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"categories", CategoryViewSet, "categories")
router.register(r"expenses", ExpenseViewSet, "expenses")
router.register(r"groups", GroupViewSet, "groups")
router.register(r"payments", PaymentViewSet, "payments")
router.register(r"teams", TeamViewSet, "teams")
router.register(r"users", UserViewSet, "users")
router.register(r"userteams", UserTeamViewSet, "userteams")

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("register", register_user),
    path("login", login_user),
]
