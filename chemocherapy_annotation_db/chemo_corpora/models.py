from django.db import models

# Create your models here.


class Chemogene(models.Model):
    gene_name = models.CharField(max_length=30, unique=True)
    description = models.CharField()

    def __str__(self) -> str:
        return self.gene_name
