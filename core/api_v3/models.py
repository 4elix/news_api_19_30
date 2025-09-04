from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from api_v1.models import News


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_created=True)
    estimation = models.PositiveIntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    content = models.TextField()
