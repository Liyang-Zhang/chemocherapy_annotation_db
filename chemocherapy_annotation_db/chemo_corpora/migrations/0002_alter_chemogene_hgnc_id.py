# Generated by Django 4.2.13 on 2024-06-11 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemo_corpora', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemogene',
            name='hgnc_id',
            field=models.TextField(unique=True),
        ),
    ]
