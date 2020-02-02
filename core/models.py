from django.db import models
from webdata import settings
import uuid

class row_news(models.Model):
	id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
	source = models.CharField(max_length=50) # news name
	url = models.TextField()
	news_no = models.CharField(max_length=50)
	title = models.TextField()
	datetime = models.DateTimeField(auto_now=True)
	author = models.TextField(null=True)
	content = models.TextField()

# class row_picture(models.Model):
# 	id = models.AutoField(unique=True)
# 	reporter = models.ForeignKey("row_news", on_delete=models.CASCADE)
# 	img = models.CharField(max_length=50)