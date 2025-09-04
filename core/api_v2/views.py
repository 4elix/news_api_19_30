from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from api_v1.models import Categories, News
from .serializers import NewsSerializer, CategoriesSerializer, FavoriteSerializer
from .models import Favorite


class NewsList(APIView):
    def get(self, request):
        queryset = News.objects.all()
        serializer = NewsSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = NewsSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NewsDetail(APIView):
    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        serializer = NewsSerializer(news, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    def get(self, request):
        queryset = Categories.objects.all()
        serializer = CategoriesSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoriesSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get(self, request, slug):
        category = get_object_or_404(Categories, category_slug=slug)
        serializer = CategoriesSerializer(category, context={'request': request})
        return Response(serializer.data)

    def put(self, request, slug):
        category = get_object_or_404(Categories, category_slug=slug)
        serializer = CategoriesSerializer(category, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, slug):
        category = get_object_or_404(Categories, category_slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleFavorite(APIView):
    # Только аутентифицированные пользователи могут вызывать функцию
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        news_id = request.data.get('news')

        if not news_id:
            return Response({'detail': 'нужно передать id новости'},
                            status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorite.objects.filter(user=user, news_id=news_id).first()
        if favorite:
            favorite.delete()
            return Response({'detail': 'Удалено из избранного'}, status=status.HTTP_200_OK)

        serializer = FavoriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Добавлено в избранное'}, status=status.HTTP_201_CREATED)


class UserFavoriteList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NewsSerializer  # Мы хотим отдать сами новости, а не Favorite

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('news')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        news_items = [favorite.news for favorite in queryset]
        serializer = self.get_serializer(news_items, many=True)
        return Response(serializer.data)
