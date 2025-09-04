from django.db import models
from django.contrib.auth.models import User
from api_v1.models import News


class Favorite(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['news', 'user']  # Защита от дубликатов
