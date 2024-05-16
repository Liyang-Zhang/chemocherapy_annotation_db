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
            gene_name = row["gene"]
            description = row["description"]

            obj, created = Chemogene.objects.update_or_create(
                gene_name=gene_name,
                defaults={"description": description},
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully"))


if __name__ == "__main__":
    pass
