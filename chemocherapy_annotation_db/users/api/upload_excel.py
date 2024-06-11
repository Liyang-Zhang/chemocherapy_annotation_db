# ruff: noqa
# users/api/upload_excel.py
import pandas as pd
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chemocherapy_annotation_db.chemo_corpora.models import Chemogene


class UploadExcel(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                for _, row in df.iterrows():
                    Chemogene.objects.update_or_create(
                        hgnc_id=row["hgnc_id"],
                        defaults={
                            "gene_symbol": row["gene_symbol"],
                            "description_cn": row["description_cn"],
                            "description_en": row["description_en"],
                            "created_at": row["created_at"],
                            "updated_at": row["updated_at"],
                            "status": row["status"],
                        },
                    )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"status": "File processed successfully"},
            status=status.HTTP_200_OK,
        )
