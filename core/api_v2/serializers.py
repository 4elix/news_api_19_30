from rest_framework import serializers
from api_v1.models import Categories, Tags, News

from .models import Favorite


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'category_name', 'category_slug']
        # Поля, доступные только для чтения (нельзя изменить через сериализатор)
        read_only_fields = ['id']

# id == pk
# pk -> primary key


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['pk', 'tag_name']
        read_only_fields = ['id']


class NewsSerializer(serializers.ModelSerializer):
    # Сериализация связанной категории (объект Category), только для чтения
    category = CategoriesSerializer(read_only=True)
    # Сериализация связанных тегов (объекты Tag), many=True так как теги в множественном числе,
    tags_new = TagsSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['id']

    # Добавляем дополнительное поле, вычисляемое методом (SerializerMethodField)
    count_symbol_desc = serializers.SerializerMethodField(method_name='len_desc')

    def len_desc(self, news: News):
        return f'Кол-во символ в описание: {len(news.desc)}'

    # Переопределяем метод update используется при PUT/PATCH запросах для обновления объекта
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.desc = validated_data.get('desc')
        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['news']
