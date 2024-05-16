from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from chemocherapy_annotation_db.chemo_corpora.views import ChemogeneViewSet
from chemocherapy_annotation_db.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("Chemogene", ChemogeneViewSet)


app_name = "api"
urlpatterns = router.urls
