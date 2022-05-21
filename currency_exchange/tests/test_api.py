"""
    Collect all tests for api calls
"""
import json
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework import status
from django.contrib.auth.hashers import check_password
from currency_exchange.models import CurrencyRates, UsersExchangeOperations
from currency_exchange.serializers import CurrencyRatesSerializer, GetUsersExchangeOperationsSerializer, \
    UserCreateSerializer


class CurrencyRatesApiTestCase(APITestCase):
    """
    Class for testing api calls
    """
    def setUp(self) -> None:
        """
        Set up data for tests
        :return:
        """
        self.user_1 = User.objects.create(username='test_username_1')
        self.user_2 = User.objects.create(username='test_username_2', password='test')
        self.user_3 = User.objects.create(username='User_test3', email='user@example.com',
                                          password='User_test3')
        self.cur_1 = CurrencyRates.objects.create(to_currency='CHF', sale_rate='32.1000',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='31.4000')
        self.cur_2 = CurrencyRates.objects.create(to_currency='CZK', sale_rate='1.3450',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='1.3150')
        self.cur_3 = CurrencyRates.objects.create(to_currency='EUR', sale_rate='33.3500',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='32.6000')
        self.cur_4 = CurrencyRates.objects.create(to_currency='GBP', sale_rate='39.1500',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='38.3500')
        self.cur_5 = CurrencyRates.objects.create(to_currency='PLN', sale_rate='7.1300',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='6.9500')
        self.cur_6 = CurrencyRates.objects.create(to_currency='USD', sale_rate='32.1800',
                                                  day_of_rate=datetime.today().date(),
                                                  purchase_rate='31.5000')
        future_date = datetime.today().date() + timedelta(days=10)
        self.cur_7 = CurrencyRates.objects.create(to_currency='CZK', sale_rate='1.4450',
                                                  purchase_rate='1.4150',
                                                  day_of_rate=datetime.today().date() + timedelta(days=1))
        self.cur_8 = CurrencyRates.objects.create(to_currency='EUR', sale_rate='34.3500',
                                                  purchase_rate='33.6000',
                                                  day_of_rate=datetime.today().date() + timedelta(days=10))
        self.cur_9 = CurrencyRates.objects.create(to_currency='PLN', sale_rate='8.1300', purchase_rate='7.9500',
                                                   day_of_rate=datetime.today().date() + timedelta(days=10))

        self.cur_10 = CurrencyRates.objects.create(to_currency='USD', sale_rate='33.1800',
                                                   purchase_rate='32.5000',
                                                   day_of_rate=future_date)

        self.user_operation_1 = UsersExchangeOperations.objects.create(currency=self.cur_1,
                                                                       count=2, user=self.user_1)
        self.user_operation_2 = UsersExchangeOperations.objects.create(currency=self.cur_2,
                                                                       count=2, user=self.user_1)
        self.user_operation_3 = UsersExchangeOperations.objects.create(currency=self.cur_1,
                                                                       count=2, user=self.user_2)

    def test_currency_rates_list(self):
        """
        Test that api return list currency rates
        :return:
        """
        rates = sorted([getattr(self, item) for item in
                 dir(self) if item.startswith('cur_')], key=lambda item: item.id)
        test_data = CurrencyRatesSerializer(rates, many=True).data

        response = self.client.get('/api/v1/rates/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_from_cur_to_cur(self):
        """
        Test that api return list currency rates filtered by currency name
        :return:
        """

        test_data = CurrencyRatesSerializer([self.cur_6, self.cur_10], many=True).data

        response = self.client.get('/api/v1/rates/?to_currency=USD')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_day_of_rate(self):
        """
        Test that api return list currency rates filtered by day of rate
        :return:
        """

        test_data = CurrencyRatesSerializer([self.cur_1, self.cur_2, self.cur_3, self.cur_4,
                                             self.cur_5, self.cur_6], many=True).data
        current_date = datetime.today().date().strftime('%Y-%m-%d')
        response = self.client.get('/api/v1/rates/', {'day_of_rate': current_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_day_of_rate_gte(self):
        """
        Test that api return list currency rates filtered by day of rate grater or equal
        :return:
        """
        test_data = CurrencyRatesSerializer([self.cur_8, self.cur_9, self.cur_10],
                                            many=True).data
        next_date = datetime.today().date() + timedelta(days=2)
        response = self.client.get('/api/v1/rates/',  {'day_of_rate_gte': next_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_day_of_rate_lte(self):
        """
        Test that api return list currency rates filtered by day of rate less or equal
        :return:
        """
        test_data = CurrencyRatesSerializer([self.cur_1, self.cur_2, self.cur_3, self.cur_4,
                                             self.cur_5, self.cur_6], many=True).data
        current_date = datetime.today().date()
        response = self.client.get('/api/v1/rates/', {'day_of_rate_lte': current_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_day_of_rate_lte_gte(self):
        """
        Test that api return list currency rates filtered by day of rate between two dates
        :return:
        """
        test_data = CurrencyRatesSerializer([self.cur_8, self.cur_9, self.cur_10],
                                            many=True).data
        low_date = datetime.today().date() + timedelta(days=2)
        high_date = datetime.today().date() + timedelta(days=11)
        response = self.client.get('/api/v1/rates/', {'day_of_rate_gte': low_date,
                                                      'day_of_rate_lte': high_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_to_currency(self):
        """
        Test filter by currency name
        :return:
        """
        test_data = CurrencyRatesSerializer([self.cur_6, self.cur_10], many=True).data
        response = self.client.get('/api/v1/rates/', {'to_currency': 'USD'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_rates_filter_by_to_currency_day_of_rate(self):
        """
        Test filter by day of rate
        :return:
        """

        test_data = CurrencyRatesSerializer([self.cur_6], many=True).data
        current_date = datetime.today().date()
        response = self.client.get('/api/v1/rates/', {'to_currency': 'USD', 'day_of_rate': current_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(test_data, response.data.get('results'))

    def test_currency_statistics(self):
        """
        Test currency statistic. Annotated field min max using date filters
        """
        test_data = [{'to_currency': 'CHF', 'min': Decimal('32.1000'), 'max': Decimal('32.1000')},
                     {'to_currency': 'CZK', 'min': Decimal('1.3450'), 'max': Decimal('1.4450')},
                     {'to_currency': 'EUR', 'min': Decimal('33.3500'), 'max': Decimal('34.3500')},
                     {'to_currency': 'GBP', 'min': Decimal('39.1500'), 'max': Decimal('39.1500')},
                     {'to_currency': 'PLN', 'min': Decimal('7.1300'), 'max': Decimal('8.1300')},
                     {'to_currency': 'USD', 'min': Decimal('32.1800'), 'max': Decimal('33.1800')}]

        low_date = datetime.today().date()
        high_date = datetime.today().date() + timedelta(days=10)
        response = self.client.get('/api/v1/currency_statistics/',
                                   {'date_filter_gte': low_date, 'date_filter_lte': high_date})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, list(response.data.get('statistics')))

    def test_get_users_operations(self):
        """
        Test that api return list operations for user who is authenticated
        :return:
        """

        url = reverse('users_exchange-list')

        operations = UsersExchangeOperations.objects.filter(user=self.user_1.id)\
            .annotate(amount_operation=models.F('count') * models.F('currency__sale_rate'))\
            .order_by('id')
        test_data = GetUsersExchangeOperationsSerializer(operations,
                                                         many=True).data

        self.client.force_login(self.user_1)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_data, response.data.get('results'))

    def test_post_users_operations(self):

        """
        Test that user create exchange operation
        :return:
        """
        self.assertEqual(2, UsersExchangeOperations.objects.filter(user=self.user_1.id).count())
        url = reverse('users_exchange-list')
        test_data = {
            "count": 5,
            "currency": self.cur_4.to_currency
        }

        json_data = json.dumps(test_data)
        self.client.force_login(self.user_1)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, UsersExchangeOperations.objects.filter(user=self.user_1.id).count())

    def test_delete_exchange_operation(self):
        """
        Test that authenticated user can delete exchange operation
        :return:
        """
        self.client.force_login(self.user_1)
        url = reverse('users_exchange-detail', args=(self.user_operation_1.id,))
        count = UsersExchangeOperations.objects.filter(user=self.user_1.id).count()
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(count-1, UsersExchangeOperations.objects.filter(user=self.user_1.id).count())

    def test_get_exchange_operation_permission(self):
        """
        Test that user has to be authenticated
        :return:
        """
        url = reverse('users_exchange-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')},
                         response.data)

    def test_user_registration_view(self):
        """
        Test that new user can be created using api
        :return:
        """
        test_data = {
            "username": "User_test",
            "email": "user@example.com",
            "password": "User_test"
        }

        json_data = json.dumps(test_data)
        response = self.client.post('/api/v1/create_user/', data=json_data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('User_test', response.data.get('username'))
        self.assertEqual('user@example.com', response.data.get('email'))
        self.assertTrue('User_test', response.data.get('password'))

    def test_user_update(self):
        """
        Test that user can be updated
        :return:
        """
        test_data = {
            "username": "Updated_name",
            "email": "user_updated@example.com"
        }
        json_data = json.dumps(test_data)
        self.client.force_login(self.user_3)
        response = self.client.put('/api/v1/retrieve_update_user/' + self.user_3.username + '/',
                                   data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_3.refresh_from_db()
        self.assertEqual("Updated_name", self.user_3.username)
        self.assertEqual("user_updated@example.com", self.user_3.email)

    def test_get_user(self):
        """
        Test that user can check his profile
        :return:
        """
        test_data = {
            "id": self.user_3.id,
            "username": "User_test3",
            "email": "user@example.com"
        }
        self.client.force_login(self.user_3)
        response = self.client.get('/api/v1/retrieve_update_user/' + self.user_3.username + '/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_get_user_not_owner(self):
        """
        Test that user has to be owner of profile
        :return:
        """
        self.client.force_login(self.user_2)
        response = self.client.get('/api/v1/retrieve_update_user/' + self.user_3.username + '/')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')},
                         response.data)

    def test_get_user_not_unauthorized(self):
        """
        Test that unauthorized user doesn't have permission to profile
        :return:
        """
        response = self.client.get('/api/v1/retrieve_update_user/' + self.user_3.username + '/')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')},
                         response.data)

    def test_change_password(self):
        """
        Test that authorized user can update password
        :return:
        """
        user = User.objects.create_user(username="New", email="new@mail.ua", password="new")

        data = {
            "old_password": "new",
            "password": "new_updated",
            "confirmed_password": "new_updated"
        }
        json_data = json.dumps(data)
        self.client.force_login(user)
        response = self.client.put('/api/v1/change_password/', data=json_data,
                                   content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(check_password('new_updated', response.data.get('password')))
