from django.db import models

class Nomenclature(models.Model):
    code = models.CharField('Код', max_length=650, null=False, primary_key=True)
    nomenclature = models.CharField('Номенклатура', max_length=650, null=False)
    units = models.CharField('Одиниці виміру', max_length=15, null=True, blank=True)
    group = models.CharField('Товарна група', max_length=50, null=True, blank=True)
    nomenclature_group = models.CharField('Номенклатурна група', max_length=50, null=True, blank=True)
    nomenclature_group_detail = models.CharField('Номенклатурна група деталізація', max_length=50, null=True, blank=True)
    brand = models.CharField('Бренд', max_length=65, null=True, blank=True)
    ntype = models.CharField('Тип', max_length=50, null=True, blank=True)
    local_foreign = models.CharField('Local/Foreign', max_length=15, null=True, blank=True)
    actual = models.BooleanField('Актуальний', default=True)
    manager = models.CharField('Менеджер', max_length=65, null=True, blank=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return self.code