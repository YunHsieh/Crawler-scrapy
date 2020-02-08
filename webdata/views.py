from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from core.models import row_news
from django.db import connection

import os
import json
import subprocess
# import sqlite3
import pandas as pd
import re

from scrapyd_api import ScrapydAPI

class index(APIView):
	def __init__(self):
		self.INDEX_VAR = {}
		pass
	def get(self , request,*args,**kwargs):
		return render(request,os.path.join('.','index.html'),self.INDEX_VAR)

class news_api(APIView):
	def __init__(self):
		self.cr_nba_content = row_news.objects.values().order_by('datetime').reverse()
		self.ALL_TABLES = connection.introspection.table_names()
		self.ALL_TABLES = [re.sub(r'tools_(.*)',r'\1',_table) for _table in list(self.ALL_TABLES) if re.search(r'(tools.*)',_table)]

	def post(self , request,*args,**kwargs):
		if kwargs.get('news_name',"") in self.ALL_TABLES:
			return JsonResponse(list(self.cr_nba_content), safe=False)
		else:
			return HttpResponse("<h1>%s</h1>" % ("Not found data"))

class scrapy_test(APIView):
	def __init__(self):
		self.scrapyd = ScrapydAPI('http://localhost:6800')
		self.dist_path = os.path.join(os.path.abspath(os.getcwd()),'dist')


	def post(self , request,*args,**kwargs):

		scrapy_settings = {
			"FEED_URI" : "file:" + os.path.join(self.dist_path, request.POST.get('spider_name','')) + ".json"
		}
		
		job_id = self.scrapyd.schedule(request.POST.get('project_name',''), 
			request.POST.get('spider_name',''),
			settings = scrapy_settings)
		# scrapyd.list_jobs('project_name')
		# run_scrapy(NBASpider)

		print(job_id)
		return HttpResponse("Succeed")
