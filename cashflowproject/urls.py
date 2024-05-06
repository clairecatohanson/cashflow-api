from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from cashflowapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"groups", GroupViewSet, "groups")
router.register(r"categories", CategoryViewSet, "categories")

urlpatterns = [path("", include(router.urls)), path("admin/", admin.site.urls)]
