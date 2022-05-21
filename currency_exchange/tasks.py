"""
    Collect all celery tasks for app currency exchange
"""
import logging
from datetime import datetime

import requests

from currency_exchange.models import CurrencyRates
from exchange_api.celery import app

logger = logging.getLogger('currency_exchange')

YEAR = datetime.now().year
MONTH = datetime.now().month
DAY = datetime.now().day

URL = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={DAY}.{MONTH}.{YEAR}'


@app.task
def download_exchange_rates():
    """
    Celery task get data from privat bank api and upload currency rates to db
    :return:
    """

    data = get_currency_rates()
    add_currency_rates_to_db(data)
    return 'Task download exchange rates executed successfully'


def get_currency_rates() -> dict:
    """
    Get request to api
    :return: Data from api
    """
    resp = requests.get(URL)
    logger.debug(f'Response is {resp.status_code}')
    return resp.json()


def add_currency_rates_to_db(data: dict) -> str:
    """
    Insert currency rates to db
    :param data: Data from api call
    :return: String notification
    """

    currant_date = datetime.strptime(data.get('date', datetime.today().date()), '%d.%m.%Y').date()
    if not CurrencyRates.objects.filter(day_of_rate=currant_date).exists():
        for currency in data.get('exchangeRate'):
            if currency.get('saleRate') and currency.get('purchaseRate'):
                record = CurrencyRates(to_currency=currency.get('currency'),
                                       sale_rate=currency.get('saleRate'),
                                       purchase_rate=currency.get('purchaseRate'))

                record.save()
        logger.debug('Rates was updated using api')
        return 'Rates was updated using api'
    else:
        logger.debug('Db contains rates for this day')
        return 'Db contains rates for this day'
