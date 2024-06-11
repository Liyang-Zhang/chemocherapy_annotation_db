from django.db import models

# Create your models here.


class Chemogene(models.Model):
    hgnc_id = models.TextField(unique=True)
    gene_symbol = models.TextField()
    description_cn = models.TextField()
    description_en = models.TextField()
    created_at = models.TextField()
    updated_at = models.TextField()
    status = models.TextField()

    def __str__(self) -> str:
        return self.gene_symbol
