# ruff: noqa
from django.core.management.base import BaseCommand
from django.db.models import Count

from chemocherapy_annotation_db.chemo_corpora.models import Chemogene


class Command(BaseCommand):
    help = "Clean duplicate ChemoGene data"

    def handle(self, *args, **kwargs):
        duplicates = (
            Chemogene.objects.values("gene_name")
            .annotate(name_count=Count("gene_name"))
            .filter(name_count__gt=1)
        )

        for duplicate in duplicates:
            objs = Chemogene.objects.filter(gene_name=duplicate["gene_name"])
            primary_obj = objs.first()
            for obj in objs[1:]:
                # 合并或删除重复数据
                # primary_obj.description += f"; {obj.description}"
                obj.delete()
            primary_obj.save()

        self.stdout.write(self.style.SUCCESS("Duplicates cleaned successfully"))


if __name__ == "__main__":
    pass
