"""
    Collect all serializers for app currency exchange
"""
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from currency_exchange.models import CurrencyRates, UsersExchangeOperations


class CurrencyRatesSerializer(ModelSerializer):
    """
    Currency rates serializer
    """
    class Meta:
        model = CurrencyRates
        fields = '__all__'


class CurrencyField(serializers.RelatedField):

    def to_representation(self, value):
        return f'Date: {value.day_of_rate} : {value.sale_rate}'


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class GetUsersExchangeOperationsSerializer(ModelSerializer):
    """
    Users exchange operations serializer
    """
    currency = serializers.SlugRelatedField(
        slug_field='to_currency',
        queryset=CurrencyRates.objects
            .filter(
            Q(day_of_rate=datetime.today().date()) |
            Q(day_of_rate=datetime.today().date() + timedelta(days=-1))
        )
    )
    amount_operation = serializers.FloatField(read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = UsersExchangeOperations
        fields = ('id', 'count', 'currency', 'user', 'amount_operation')


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating user
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """

        return make_password(value)


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=30, write_only=True)
    password = serializers.CharField(required=True, max_length=30)
    confirmed_password = serializers.CharField(required=True, max_length=30,write_only=True)

    def validate(self, data):
        """
        Check user password before changing. Check that  password and confirmed_password equal
        """
        # add here additional check for password strength if needed
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})

        if data.get('confirmed_password') != data.get('password'):
            raise serializers.ValidationError({'password': 'Password must be confirmed correctly.'})

        return data

    def update(self, instance, validated_data):
        """
        Update user password
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        pass
