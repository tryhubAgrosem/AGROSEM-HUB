# Generated by Django 4.0.2 on 2022-02-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('code', models.CharField(max_length=650, primary_key=True, serialize=False, verbose_name='Код')),
                ('nomenclature', models.CharField(max_length=650, verbose_name='Номенклатура')),
                ('units', models.CharField(blank=True, max_length=15, null=True, verbose_name='Одиниці виміру')),
                ('group', models.CharField(blank=True, max_length=50, null=True, verbose_name='Товарна група')),
                ('nomenclature_group', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номенклатурна група')),
                ('nomenclature_group_detail', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номенклатурна група деталізація')),
                ('brand', models.CharField(blank=True, max_length=65, null=True, verbose_name='Бренд')),
                ('ntype', models.CharField(blank=True, max_length=50, null=True, verbose_name='Тип')),
                ('local_foreign', models.CharField(blank=True, max_length=15, null=True, verbose_name='Local/Foreign')),
                ('actual', models.BooleanField(default=True, verbose_name='Актуальний')),
                ('manager', models.CharField(blank=True, max_length=65, null=True, verbose_name='Менеджер')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
    ]
