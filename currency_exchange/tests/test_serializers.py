"""
    Collect all tests for serializers
"""

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from currency_exchange.models import CurrencyRates, UsersExchangeOperations
from currency_exchange.serializers import CurrencyRatesSerializer, GetUsersExchangeOperationsSerializer, \
    UserCreateSerializer, UserPasswordChangeSerializer


class SerializersTestCase(TestCase):
    """
    Class for testing serializers
    """

    def setUp(self):
        """
        Set up data for tests
        :return:
        """
        self.user_1 = User.objects.create(username='test_username_1')
        self.user_2 = User.objects.create(username='test_username_2')
        self.user_3 = User.objects.create(username='User_test', email='user@example.com',
                                          password='User_test')
        self.cur_1 = CurrencyRates.objects.create(to_currency='CHF', sale_rate='32.1000',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='31.4000')
        self.cur_2 = CurrencyRates.objects.create(to_currency='CZK', sale_rate='1.3450',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='1.3150')
        self.user_operation_1 = UsersExchangeOperations.objects.create(currency=self.cur_1,
                                                                       count=2, user=self.user_1)
        self.user_operation_2 = UsersExchangeOperations.objects.create(currency=self.cur_2,
                                                                       count=2, user=self.user_1)
        self.user_operation_3 = UsersExchangeOperations.objects.create(currency=self.cur_1,
                                                                       count=2, user=self.user_2)

    def test_currency_rates_serializer(self):
        """
        Test rates serializer
        :return:
        """
        result = CurrencyRatesSerializer([self.cur_1, self.cur_2], many=True).data
        expected_data = [
            {
                "id": self.cur_1.id,
                "from_currency": "UAH",
                "to_currency": "CHF",
                "day_of_rate": datetime.today().date().strftime("%Y-%m-%d"),
                "sale_rate": "32.1000",
                "purchase_rate": "31.4000"
            },
            {
                "id": self.cur_2.id,
                "from_currency": "UAH",
                "to_currency": "CZK",
                "day_of_rate": datetime.today().date().strftime("%Y-%m-%d"),
                "sale_rate": "1.3450",
                "purchase_rate": "1.3150"
            }
        ]
        self.assertEqual(expected_data, result)

    def test_get_users_exchange_operations_serializer(self):
        """
        Test users exchange operations serializer
        :return:
        """
        operations = UsersExchangeOperations.objects.filter(user=self.user_1.id) \
            .annotate(amount_operation=models.F('count') * models.F('currency__sale_rate')) \
            .order_by('id')
        test_data = GetUsersExchangeOperationsSerializer(operations,
                                                         many=True).data
        expected_data = [
            {
                "id": self.user_operation_1.id,
                "count": 2,
                "currency": "CHF",
                "user": "test_username_1",
                "amount_operation": 64.2,
            },
            {
                "id": self.user_operation_2.id,
                "count": 2,
                "currency": "CZK",
                "user": "test_username_1",
                "amount_operation": 2.69,
            }
        ]
        self.assertEqual(expected_data, test_data)

    def test_create_user_serializer(self):
        """
        Test create user serializer
        :return:
        """
        result = UserCreateSerializer(self.user_3).data
        expected_data = {
            "username": "User_test",
            "email": "user@example.com",
            "password": 'User_test'
        }
        self.assertEqual(expected_data, result)
