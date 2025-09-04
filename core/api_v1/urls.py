from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.categories_list, name='categories_list'),
    path('tags/', views.tags_list),
    path('category/<slug:slug>/', views.category),
    path('tag/<int:pk>/', views.tag),
    path('news/', views.news_list),
    path('news/<int:pk>/', views.news),
]
# python manage.py runserver
