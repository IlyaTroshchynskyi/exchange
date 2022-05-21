"""
    Collect all urls for app currency exchange
"""

from django.urls import path
from rest_framework.routers import SimpleRouter

from currency_exchange.views import CurrencyRatesViewSet, CurrencyRatesStatistic, UsersExchangeOperationsView, \
    UserRegistrationView, APIChangePasswordView, UserRetrieveUpdateAPIView, auth

urlpatterns = [
    path('currency_statistics/', CurrencyRatesStatistic.as_view()),
    path('change_password/', APIChangePasswordView.as_view())
]

router = SimpleRouter()
router.register(r'rates', CurrencyRatesViewSet)
router.register(r'users_exchange', UsersExchangeOperationsView, basename='users_exchange')
router.register(r'create_user', UserRegistrationView)
router.register(r'retrieve_update_user', UserRetrieveUpdateAPIView)


urlpatterns += router.urls