from rest_framework import viewsets

from .models import Chemogene
from .serializers import ChemogeneSerializer


class ChemogeneViewSet(viewsets.ModelViewSet):
    queryset = Chemogene.objects.all()
    serializer_class = ChemogeneSerializer
