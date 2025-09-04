from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Categories(models.Model):
    category_name = models.CharField(max_length=255)
    category_slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.category_name


class Tags(models.Model):
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name


class News(models.Model):
    title = models.CharField(max_length=255)
    card_desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/news/', null=True, blank=True)
    desc = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    tags_new = models.ManyToManyField(Tags)
    rating = models.FloatField(default=0, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(5.0)
    ])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    age_limited = models.IntegerField(default=18)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

