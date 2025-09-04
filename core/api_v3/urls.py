from .views import *
from django.urls import path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .swagger_settings import urlpatterns as url_swagger

# Импортируем роутеры для DRF с поддержкой вложенных маршрутов (Nested Routers)

# Создаём экземпляр стандартного роутера, который будет автоматически
# генерировать URL'ы для ViewSet'ов

router = routers.DefaultRouter()

# Регистрируем маршрут /news/ для NewsViewSet
# basename используется для формирования имён маршрутов (например, news-list, news-categories)

router.register('news', NewsViewSet, basename='news')
router.register('categories', CategoryViewSet, basename='category')

# Создаём вложенный роутер для новостей
# lookup='news' означает, что в URL будет использоваться параметр news_pk (например: /news/1/comments/
news_router = routers.NestedDefaultRouter(router, 'news', lookup='news')

# Регистрируем вложенный маршрут "comments" для каждой новости
news_router.register('comments', CommentViewSet, basename='news-comments')

register_path = [
    path('register/', RegisterView.as_view(), name='register'),  # регистрация
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # вход (JWT токен)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновление токена
]

# Получаем все сгенерированные URL'ы роутера и присваиваем их в переменную urlpatterns для Django
urlpatterns = router.urls + register_path + url_swagger + news_router.urls
