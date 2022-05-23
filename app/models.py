from django.db import models

# Create your models here.
class Company_info(models.Model):
    id_company_rpn = models.IntegerField(max_length=15, verbose_name='id компании на rpn', blank=True)
    number_license = models.CharField(max_length=50, verbose_name='Номер лицензии')
    date_of_issue = models.DateField(max_length=50, verbose_name='Дата выдачи')
    status = models.CharField(max_length=250, verbose_name='Статус')
    issued_by = models.CharField(max_length=250, verbose_name='Кем выдан')
    termination_order = models.CharField(max_length=250, verbose_name='Приказ о прекращении')
    licensee = models.CharField(max_length=250, verbose_name='Лицензиат')
    address = models.CharField(max_length=250, verbose_name='Адрес', null=True)
    inn = models.IntegerField(max_length=50, verbose_name='ИНН')
    type_of_work = models.CharField(max_length=250, verbose_name='Вид работ')
    hazard_class = models.CharField(max_length=250, verbose_name='Класс опасности')