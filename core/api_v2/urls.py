from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsList.as_view()),
    path('news/<int:pk>/', views.NewsDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('category/<slug:slug>/', views.CategoryDetail.as_view()),
    path('favorite/toggle/', views.ToggleFavorite.as_view()),
    path('favorites/', views.UserFavoriteList.as_view())
]