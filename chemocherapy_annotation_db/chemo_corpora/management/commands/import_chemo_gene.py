# ruff: noqa
import pandas as pd
from django.core.management.base import BaseCommand

from chemocherapy_annotation_db.chemo_corpora.models import Chemogene


class Command(BaseCommand):
    help = "Import Chemo gene corpora from excel file"

    def add_arguments(self, parser):
        parser.add_argument("excel_file", type=str, help="The path to the Excel file")

    def handle(self, *args, **kwargs):
        excel_file = kwargs["excel_file"]
        df = pd.read_excel(excel_file)

        for _, row in df.iterrows():
            hgnc_id = row["hgnc_id"]
            gene_symbol = row["gene_symbol"]
            description_cn = row["description_cn"]
            description_en = row["description_en"]
            created_at = row["created_at"]
            updated_at = row["updated_at"]
            status = row["status"]

            obj, created = Chemogene.objects.update_or_create(
                gene_symbol=gene_symbol,
                hgnc_id=hgnc_id,
                defaults={
                    "description_cn": description_cn,
                    "description_en": description_en,
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "status": status,
                },
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))


if __name__ == "__main__":
    pass
