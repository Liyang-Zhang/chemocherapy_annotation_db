from rest_framework import serializers

from .models import Chemogene


class ChemogeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemogene
        fields = "__all__"
