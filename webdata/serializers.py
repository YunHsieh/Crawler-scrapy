from rest_framework import serializers
from core.models import *
from rest_framework.fields import CurrentUserDefault

class CrawlerSerializers(serializers.ModelSerializer):
	def create(self, validated_data):
		return row_news.objects.create(**validated_data)

	class Meta:
		model = row_news
		fields = (
			'news_name',
			'url',
			'news_no',
			'title',
			'content',
			'datetime',
			'author',
			'shortened_title',
			'images',
			'category',
			'keywords'
		)

# class KpiGroupSerializers(serializers.ModelSerializer):
# 	def create(self, validated_data):
# 		validated_data['creator_id'] = self.context.user.id
# 		return kpi_group.objects.create(**validated_data)


# 	class Meta:
# 		model = kpi_group
# 		fields = (
# 			'group_name', 
# 			'group_category',
# 			'creator_id',
# 		)
# 	extra_kwargs = {'kpi_name': {'read_only': True},'group_name': {'read_only': True}}

