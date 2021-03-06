# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.utils import timezone
from django.core import serializers
from django.db import connection
from itertools import groupby
from django.db.models import Count
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware

import dateutil.parser
import os.path
import json
import codecs
import pytz
from base64 import b64encode, b64decode
from datetime import datetime, date
from server.models import St_folio, ST, Folio, St_work

from django.shortcuts import render
from django.utils.decorators import decorator_from_middleware
from filter_phone_middleware import FilterPhone
# Create your views here.
def index(request):
    return HttpResponse("Hello, world")

@FilterPhone
def insertData(request):
    print "REQUEST ---> ", request
    if request.method == "POST":
        data = None
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            data = body
        except ValueError:
            response = {
                "message":"error",
                "status":406,
            }
            return HttpResponse(json.dumps(response), content_type='application/json')

        imgBase64 = None
        st = None
        folio = None
        lat = None
        lng = None
        note = None
        date = None
        phone = None
        try:
            phone = request.META['HTTP_TOKEN_NUMBER']
            imgBase64 = data['FileName']
            date = data['CreatedOn']
            st = data['ST_string']
            folio = data['Folio_string']
            lat = data['Latitude']
            lng = data['Longitude']
            note = data['Note']
        except:
            response = {
             "message":"Error in params",
             "status":406,
            }
            return HttpResponse(json.dumps(response),content_type='application/json')
        st = str(st)
        folio = str(folio)
        lat = float(lat)
        lng = float(lng)
        note = str(note)
        phone = str(phone)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_time_path = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        date_ = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        date_parse = date_.strftime("%Y-%m-%d %H:%M:%S")
        date_parse_path = date_.strftime("%Y-%m-%d-%H-%M-%S")
        #I NEED ADD THIS DATE 'DATE_PARSE' TO PATH AND DATE INSERT
        # Create path to a image
        path="media/images/"+str(date_parse_path)+str(data['ST_string'])+str(data['Folio_string'])+".png"
        #print "time -> ", timezone.localtime(timezone.now())
        try:
            st_tmp=ST.objects.get(name=st)
            folio_tmp=Folio.objects.get(name=folio)
            st_temp = St_folio.objects.filter(idST=st_tmp,idFolio=folio_tmp).first()
            pro = st_temp.idPro
            st_folio=St_folio.objects.create(idST=st_tmp,idFolio=folio_tmp, idPro=pro, date=date_parse, path_img=path,lng=lng,lat=lat,note=note, phone=phone)
            work = St_work.objects.get(idSTFolio=st_temp.id)
            St_work.objects.create(idObra=work.idObra, idSTFolio=st_folio)
        except:
            response = {
             "message":"These data already existed",
             "status":400,
            }
            return HttpResponse(json.dumps(response),content_type='application/json')

        #Recieve data
        #Insert image in route path
        try:
            with open(path, "wb") as fh:
                fh.write(imgBase64.decode('base64'))
        except:
            response = {
             "message":"Error with base64 code",
             "status":400,
            }
            return HttpResponse(json.dumps(response),content_type='application/json')
        response = {
         "message":None,
         "status":200,
        }
        return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        response = {
            "message":"error",
            "status":404,
        }
        return HttpResponse(json.dumps(response), content_type='application/json')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type %s not serializable" % type(obj))

@FilterPhone
def getSTFolios(request):
    print "REQUEST ----> ", request
    if request.method == "GET":
        rows = None
        st_database = None
        try:
            st_ = St_work.objects.all().exclude(idSTFolio__idST__isnull=True).exclude(idSTFolio__idFolio__isnull=True).order_by('idSTFolio__idST')
            if (len(st_) == 0):
                response = {
                    "message":"error",
                    "status":404,
                }
                return HttpResponse(json.dumps(response), content_type='application/json', status=404)
            dct = {k.name: [x.idSTFolio.idFolio.name for x in g] for k, g in groupby(st_, key=lambda q: q.idSTFolio.idST)}

        except:
            response = {
                "message":"error",
                "status":404,
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        json_data = json.dumps([dct], default=json_serial)
        list_res = []
        for ix in dct:
            list_folios = []
            for iy in dct[ix]:
                list_folios.append(iy)
            tmp_list = list(set(list_folios))
            list_folios = []
            for value in tmp_list:
                list_folios.append({"number":value})
            list_res.append({"st":ix, "folios":list_folios})

        return HttpResponse(json.dumps(list_res), content_type="application/json")
    else:
        response = {
            "message":"error",
            "status":404,
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


def dataFilter(request):
    print "REQUEST ----> ", request
    if request.method == "GET":
        rows = None
        work_database = St_work.objects.all().filter(idSTFolio__path_img__isnull=False).filter(idSTFolio__idPro__isnull=False).filter(idSTFolio__idST__isnull=False).filter(idSTFolio__idFolio__isnull=False)

        st_=work_database.values("idSTFolio__idST").annotate(Count("idSTFolio__idST"))
        folio_ = work_database.values("idSTFolio__idFolio").annotate(Count("idSTFolio__idFolio"))
        obra_ = work_database.values("idObra").annotate(Count('idObra'))
        profesional_ = work_database.values("idSTFolio__idPro").annotate(Count("idSTFolio__idPro"))
        resp = {"data":[]}
        st_list = {"st":[]}
        folio_list = {"folio":[]}
        obra_list = {"obra":[]}
        profesional_list = {"profesional":[]}
        for ix in st_:
            st_list["st"].append(str(ix['idSTFolio__idST']))
        for ix in folio_:
            folio_list["folio"].append(str(ix['idSTFolio__idFolio']))
        for ix in obra_:
            obra_list["obra"].append(str(ix['idObra']))
        for ix in profesional_:
            profesional_list["profesional"].append(str(ix['idSTFolio__idPro']))
        resp["data"].append(st_list)
        resp["data"].append(folio_list)
        resp["data"].append(obra_list)
        resp["data"].append(profesional_list)
        json_data = json.dumps(resp, default=json_serial)
        return HttpResponse(json_data, content_type="application/json")
    else:
        response = {
            "message":"error",
            "status":404,
        }
        return HttpResponse(json.dumps(response), content_type='application/json')


def getFolioOfST(request):
    print "REQUEST ----> ", request
    if request.method == "GET":
        try:
            st_input = request.GET['st']
        except:
            response = {
             "message":"Error in params",
             "status":406,
            }
            return HttpResponse(json.dumps(response),content_type='application/json')

        stfolio_database = St_folio.objects.filter(idST=st_input)
        if len(stfolio_database) == 0:
            response = {
                "message":"ST not exists",
                "status":400,
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        folio_ = stfolio_database.values("idFolio")
        if len(folio_) == 0:
            response = {
                "message":"Not contains folios",
                "status":200,
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        resp = []
        for ix in folio_:
            if str(ix['idFolio']) != "None":
                resp.append({"folio":str(ix['idFolio'])})
        if len(resp) == 0:
            response = {
                "message":"Not contains folios",
                "status":400,
            }
            return HttpResponse(json.dumps(response), content_type='application/json')
        else:
            json_data = json.dumps(resp, default=json_serial)
            response = {
                "data":resp,
                "status":200,
            }
            return HttpResponse(json.dumps(response), content_type="application/json");
    else:
        response = {
            "message":"error",
            "status":404,
        }
        return HttpResponse(json.dumps(response), content_type='application/json')

def get_aware_datetime(date_str):
    ret = parse_datetime(date_str)
    if not is_aware(ret):
        ret = make_aware(ret)
    return ret

def dataTable(request):
    if request.method == "POST":
        print "[dataTable request] ", request
        data = None
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
        except ValueError:
            response = {
                "message":"error",
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=406)
        start = None
        end = None
        obra = None
        st = None
        folio = None
        profesional = None
        try:
            start = data['start']
            end = data['end']
            obra = data['obra']
            st = data['st']
            folio = data['folio']
            profesional = data['profesional']
        except:
            response = {
             "message":"Error in params",
            }
            return HttpResponse(json.dumps(response),content_type='application/json',status=406)
        start = str(start)
        end = str(end)
        obra = str(obra)
        st = str(st)
        folio = str(folio)
        profesional = str(profesional)
        start = parse_datetime(start)
        end = parse_datetime(end)
        photos = None

        try:
            photos = St_work.objects.filter(idSTFolio__idPro__isnull=False).filter(idSTFolio__idST__isnull=False).filter(idSTFolio__idFolio__isnull=False).order_by('-idSTFolio__date')
            photos = photos.exclude(idSTFolio__path_img='')
            if start != None and end != None:
                photos=photos.filter(idSTFolio__date__range=[start, end])
            if obra != "":
                photos=photos.filter(idObra__name=obra)
            if st != "":
                photos=photos.filter(idSTFolio__idST__name=st)
            if folio != "":
                photos=photos.filter(idSTFolio__idFolio__name=folio)
            if profesional != "":
                photos=photos.filter(idSTFolio__idPro__name=profesional)
        except:
            response = {
             "message":"No exists data",
             }
            return HttpResponse(json.dumps(response),content_type='application/json',status=400)
        '''
        for ix in photos:
            encoded_string = None
            text = None
            print "./"+str(ix.idSTFolio.path_img)
            with open("./"+str(ix.idSTFolio.path_img), "rb") as image_file:
                #encoded_string = image_file.read()
                header = image_file.read(2)
                text = image_file.read().decode('utf-16')
                ix.idSTFolio.path_img = text

        try:
            for ix in photos:
                encoded_string = None
                print "./"+str(ix.idSTFolio.path_img)
                with open("./"+str(ix.idSTFolio.path_img), "rb","utf-16") as image_file:
                    encoded_string = image_file.read()
                    ix.idSTFolio.path_img = encoded_string
        except:
            response = {
             "message":"Error with base64 code",
            }
            return HttpResponse(json.dumps(response),content_type='application/json',status=400)
        '''
        '''
        try:
            with open(valid_image, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except IOError:
            red = Image.new('RGBA', (1, 1), (255,0,0,0))
            response = HttpResponse(content_type="image/jpeg")
            red.save(response, "JPEG")
            return response
        '''
        data = []
        for ix in photos:
            data.append({"foto":ix.idSTFolio.path_img,
                        "obra":ix.idObra.name,
                        "st":ix.idSTFolio.idST.name,
                        "folio":ix.idSTFolio.idFolio.name,
                        "profesional":ix.idSTFolio.idPro.name,
                        "phone":ix.idSTFolio.phone,
                        "date":ix.idSTFolio.date,
                        "lat":ix.idSTFolio.lat,
                        "lng":ix.idSTFolio.lng,
                        "note":ix.idSTFolio.note})
        #print data
        response = {
         "data":data,
        }
        return HttpResponse(json.dumps(response, default=json_serial),content_type='application/json',status=200)
    else:
        response = {
            "message":"error",
        }
        return HttpResponse(json.dumps(response), content_type='application/json',status=404)
