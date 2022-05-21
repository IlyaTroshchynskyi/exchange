"""
    Collect all tests for celery tasks
"""

from currency_exchange.tasks import download_exchange_rates
from rest_framework.test import APITestCase

#
# class TestAddTask(APITestCase):
#
#     def test_task_download_exchange_rates(self):
#         """
#         Test celery tasks which upload currency rates to db
#         :return:
#         """
#         results = download_exchange_rates.apply()
#         self.assertEqual(results.get(), 'Task download exchange rates executed successfully')
#         self.assertEqual(results.state, 'SUCCESS')
