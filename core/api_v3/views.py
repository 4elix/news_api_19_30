from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView

from .models import Comments
from .pagination import NewsPagination
from .serializers import RegisterSerializer, CommentsSerializer
from api_v1.models import News, Categories
from api_v2.serializers import NewsSerializer, CategoriesSerializer, FavoriteSerializer


# Создаём ViewSet на основе DRF ModelViewSet, чтобы автоматически получить
# CRUD-операции (CREATE, RETRIEVE, UPDATE, DELETE)
class NewsViewSet(ModelViewSet):
    # Указываем сериализатор, который будет преобразовывать объекты модели в JSON и обратно
    serializer_class = NewsSerializer

    # Задаём набор данных все записи модели News
    queryset = News.objects.all()
    pagination_class = NewsPagination

    # Подключаем фильтры: поиск (SearchFilter) и сортировка (OrderingFilter)
    filter_backends = [SearchFilter, OrderingFilter]

    # Поля, по которым будет работать поиск здесь поиск по заголовку
    search_fields = ['title']

    # Поля, по которым можно будет сортировать здесь сортировка по рейтингу
    ordering_fields = ['rating']

    # Переопределяем метод для передачи дополнительного контекста в сериализатор
    def get_serializer_context(self):
        # Передаём объект запроса в сериализатор
        return {'request': self.request}


class CategoryViewSet(ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['category_name']
    ordering_fields = ['pk']

    def get_serializer_context(self):
        return {'request': self.request}


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # доступно всем
    serializer_class = RegisterSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comments.objects.filter(news_id=self.kwargs['news_pk']).order_by('-datetime_created')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            news_id=self.kwargs['news_pk']
        )
