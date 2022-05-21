"""
    Collect django models for app currency exchange
"""

from django.contrib.auth.models import User
from django.db import models

from django.utils.datetime_safe import date


class CurrencyRates(models.Model):
    """
    Model look for currency exchange rates
    """
    from_currency = models.CharField(max_length=20, default='UAH')
    to_currency = models.CharField(max_length=20)
    day_of_rate = models.DateField(default=date.today)
    sale_rate = models.DecimalField(max_digits=6, decimal_places=4)
    purchase_rate = models.DecimalField(max_digits=6, decimal_places=4)

    def __str__(self):
        """
        Representation of model
        :return: str
        """
        return f'Rate:UAN:{self.to_currency}={self.purchase_rate}:' \
               f'{self.sale_rate}:{self.day_of_rate}'


class UsersExchangeOperations(models.Model):
    """
    Model look for currency exchange user history and currency operations
    """
    currency = models.ForeignKey(CurrencyRates, on_delete=models.SET_NULL,
                                 null=True, related_name='operations')
    count = models.IntegerField('Count_exchange', blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             related_name='exchanges')

    def __str__(self):
        """
        Representation of model
        :return: str
        """
        return f'Rate: {self.id}:{self.currency}:{self.count}={self.user}:'
