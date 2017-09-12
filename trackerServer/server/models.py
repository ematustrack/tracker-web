# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.db import models


#Base class
class Folio(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    def __str__(self):
        return self.name

class ST(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    def __str__(self):
        return self.name
class Work(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    def __str__(self):
        return self.name

#Union class
class St_folio(models.Model):
    idST = models.ForeignKey('ST', blank=True, null=True)
    idFolio = models.ForeignKey('Folio', blank=True, null=True)
    class Meta:
        unique_together = (('idST', 'idFolio', 'path_img'),)
        verbose_name_plural = 'ST y Folios asociados'
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
        verbose_name_plural = 'Obras asociadas'
    idObra = models.ForeignKey('Work', on_delete=models.CASCADE)
    idSTFolio = models.OneToOneField('St_folio', on_delete=models.CASCADE)
    def __str__(self):
        return self.idObra.name + "/"+str(self.idSTFolio)

class Pro(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.name
