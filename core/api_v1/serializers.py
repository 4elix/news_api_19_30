from rest_framework import serializers
from .models import Categories, Tags, News


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['pk', 'category_name', 'category_slug']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['pk', 'tag_name']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
