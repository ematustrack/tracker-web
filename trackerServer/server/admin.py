# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *

class StFolioAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		st_input = obj.idST
		result = None
		try:
			result=St_work.objects.filter(idSTFolio__idST=st_input).first()
			if result != None:
				work=Work(name=result.idObra.name)
				obj.save()
				st=St_work(idObra=work, idSTFolio=obj)
				st.save()
			else:
				obj.save()
		except:
			obj.save()

admin.site.register(St_work)
admin.site.register(St_folio)

admin.site.register(Pro)
admin.site.register(ST)
admin.site.register(Folio)
admin.site.register(Work)
