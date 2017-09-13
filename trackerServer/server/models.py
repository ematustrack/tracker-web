# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.db import models


#Base class
class Folio(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    class Meta:
        verbose_name_plural = '6. Creación de Folio'
    def __str__(self):
        return self.name

class ST(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    class Meta:
        verbose_name_plural = '5. Creación de ST'
    def __str__(self):
        return self.name
class Work(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    class Meta:
        verbose_name_plural = '4. Creación de Obra'
    def __str__(self):
        return self.name

#Union class
class St_folio(models.Model):
    idST = models.ForeignKey('ST', blank=True, null=True)
    idFolio = models.ForeignKey('Folio', blank=True, null=True)
    class Meta:
        unique_together = (('idST', 'idFolio', 'path_img'),)
        verbose_name_plural = '2. ST y Folios asociados'
    idPro = models.ForeignKey('Pro', blank=True, null=True)
    path_img = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        if self.date != None:
            return str(self.idST) + str(self.idFolio)+"-"+str(self.date)
        else:
            return str(self.idST) + str(self.idFolio)+" => PLANTILLA"

class St_work(models.Model):
    class Meta:
        unique_together = (('idObra', 'idSTFolio'),)
        verbose_name_plural = '1. Obras asociadas'
    idObra = models.ForeignKey('Work', on_delete=models.CASCADE)
    idSTFolio = models.OneToOneField('St_folio', on_delete=models.CASCADE)
    def __str__(self):
        return self.idObra.name + "/"+str(self.idSTFolio)

class Pro(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    class Meta:
        verbose_name_plural = '3. Creación de Profesional'
    def __str__(self):
        return self.name
