from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from chemocherapy_annotation_db.chemo_corpora.views import ChemogeneViewSet
from chemocherapy_annotation_db.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("Chemogene", ChemogeneViewSet)


app_name = "api"
urlpatterns = router.urls

# 添加一个新的 URL 路径来获取 CSRF 令牌
urlpatterns += [
    path("csrf/", ChemogeneViewSet.as_view({"get": "csrf"}), name="csrf"),
]
