# Generated by Django 4.2.13 on 2024-06-11 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chemogene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hgnc_id', models.TextField()),
                ('gene_symbol', models.TextField()),
                ('description_cn', models.TextField()),
                ('description_en', models.TextField()),
                ('created_at', models.TextField()),
                ('updated_at', models.TextField()),
                ('status', models.TextField()),
            ],
        ),
    ]
