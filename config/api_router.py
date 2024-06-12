from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from chemocherapy_annotation_db.chemo_corpora.views import ChemogeneViewSet
from chemocherapy_annotation_db.users.api.upload_excel import UploadExcel
from chemocherapy_annotation_db.users.api.views import LoginView
from chemocherapy_annotation_db.users.api.views import LogoutView
from chemocherapy_annotation_db.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("Chemogene", ChemogeneViewSet)


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("csrf/", ChemogeneViewSet.as_view({"get": "csrf"}), name="csrf"),
    path("upload_excel/", UploadExcel.as_view(), name="upload_excel"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
