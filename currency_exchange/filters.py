"""
    Collect all filters for app currency exchange
"""

from django_filters import rest_framework as filters

from currency_exchange.models import CurrencyRates


class FilterCurrency(filters.FilterSet):
    """
    Filter for view CurrencyRatesViewSet
    """
    day_of_rate_lte = filters.DateFilter(field_name='day_of_rate', lookup_expr='lte')
    day_of_rate_gte = filters.DateFilter(field_name='day_of_rate', lookup_expr='gte')

    class Meta:
        model = CurrencyRates
        fields = ['from_currency', 'to_currency', 'day_of_rate', 'day_of_rate_lte', 'day_of_rate_gte']
