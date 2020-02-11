from django.db import models
from webdata import settings
import uuid

class row_news(models.Model):
	id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
	news_name = models.CharField(max_length=50) # news name
	url = models.TextField()
	news_no = models.CharField(max_length=50)
	title = models.TextField()
	content = models.TextField()
	datetime = models.DateTimeField()
	author = models.TextField(null=True, blank=True)
	shortened_title = models.CharField(max_length=100, null=True, blank=True)
	images = models.TextField(null=True, blank=True)
	category = models.CharField(max_length=10)
	keywords = models.CharField(max_length=100, null=True, blank=True)

	class Meta:
		unique_together = (('news_name','news_no'))
	

# class row_picture(models.Model):
# 	id = models.AutoField(unique=True)
# 	reporter = models.ForeignKey("row_news", on_delete=models.CASCADE)
# 	img = models.CharField(max_length=50)