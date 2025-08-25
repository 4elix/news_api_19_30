from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Comments


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # write_only=True -> поле можно отправить на сервер, но оно не вернётся в ответе (безопасность)
    # required=True -> обязательное поле
    # validators=[validate_password] -> проверка на сложность пароля (Django password validators)

    class Meta:
        # работаем с встроенной моделью пользователя Django
        model = User

        # указываем поля, которые будут приходить от клиента и валидироваться
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']

    def validate(self, attrs):
        # Метод общей валидации: проверяем, что пароли совпадают
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})

        return attrs

    def create(self, validated_data):
        # Метод создания нового пользователя
        validated_data.pop('password2')  # удаляем поле подтверждения пароля, оно в БД не нужно
        user = User.objects.create_user(**validated_data)  # создаём пользователя с хэшированием пароля
        return user


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
