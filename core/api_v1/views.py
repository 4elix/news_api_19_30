from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Categories, Tags, News
from .serializers import CategoriesSerializer, TagsSerializer, NewsSerializer

# GET / POST / PUT / PATCH / DELETE
# GET -> Получение данных с сервера
# POST -> Создание нового ресурса
# PUT -> Полное обновление ресурса
# PATCH -> Частичное обновление ресурса
# DELETE -> Удаление ресурса


@api_view(['GET', 'POST'])
def categories_list(request):
    if request.method == 'GET':
        # получаем данные
        queryset = Categories.objects.all()  # [{pk: 1, category_name: ..., category_slug: ...}, {}]
        # сериализуем данные
        serializers = CategoriesSerializer(queryset, many=True, context={'request': request})
        # с помощью класса Response, мы отображаем результат сериализации
        return Response(serializers.data)
    elif request.method == 'POST':
        # получаем данные из запроса, передаем в класс сериализация
        serializer = CategoriesSerializer(data=request.data, context={'request': request})
        # проверяем на валидность
        # raise_exception=True -> если данные не прошли проверку, получаем ошибку. То есть не делаем
        # лишнее условие
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def tags_list(request):
    if request.method == 'GET':
        queryset = Tags.objects.all()
        serializers = TagsSerializer(queryset, many=True, context={'request': request})
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = TagsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category(request, slug):
    queryset = get_object_or_404(Categories, category_slug=slug)
    context = {'request': request}

    if request.method == 'GET':
        serializer = CategoriesSerializer(queryset, context=context)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategoriesSerializer(queryset, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def tag(request, pk):
    queryset = get_object_or_404(Tags, pk=pk)
    context = {'request': request}

    if request.method == 'GET':
        serializer = TagsSerializer(queryset, context=context)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TagsSerializer(queryset, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def news_list(request):
    if request.method == 'GET':
        queryset = News.objects.all()
        serializers = NewsSerializer(queryset, many=True, context={'request': request})
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = NewsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def news(request, pk):
    queryset = get_object_or_404(News, pk=pk)
    context = {'request': request}

    if request.method == 'GET':
        serializer = NewsSerializer(queryset, context=context)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NewsSerializer(queryset, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)