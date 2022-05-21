"""
    Collect all views for app currency exchange
"""

import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Avg, Min, Max
from django.shortcuts import render

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet

from currency_exchange.filters import FilterCurrency
from currency_exchange.models import CurrencyRates, UsersExchangeOperations
from currency_exchange.permissions import IsOwner
from currency_exchange.serializers import CurrencyRatesSerializer, GetUsersExchangeOperationsSerializer, \
    CreateUsersExchangeOperationsSerializer, UserCreateSerializer, UserSerializer, UserPasswordChangeSerializer

logger = logging.getLogger('currency_exchange')


class CurrencyRatesViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    View look for currency rates with filters by currency name and by date of rate
    """
    queryset = CurrencyRates.objects.all()
    serializer_class = CurrencyRatesSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = FilterCurrency
    # permission_classes = (IsAuthenticated, )

    @extend_schema(
        parameters=[

            OpenApiParameter("day_of_rate", OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
                             description='Set the period for getting currency rates'),
            OpenApiParameter("day_of_rate_lte", OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
                             description='Set the period for getting currency rates'),
            OpenApiParameter("day_of_rate_gte", OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
                             description='Set the period for getting currency rates'),
            OpenApiParameter("to_currency", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description='Set the currency code for filtering currency'),
        ])
    def list(self, request, *args, **kwargs):
        logger.debug(f'User: {request.user} get response by url {request.get_full_path()}'
                     f'with args: {args} {kwargs}')
        return super().list(request, *args, **kwargs)


class CurrencyRatesStatistic(APIView):
    """
    View to get statistics during some periods by currency name.
    Statistic like min and max
    """

    # permission_classes = (IsAuthenticated, )

    @extend_schema(
        parameters=[

            OpenApiParameter("day_of_rate_lte", OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
                             description='Set the period for getting min, max'),
            OpenApiParameter("day_of_rate_gte", OpenApiTypes.DATETIME, OpenApiParameter.QUERY,
                             description='Set the period for getting min, max'),
        ])
    def get(self, request, format=None):
        """
        Return min max rates for all currency according to filter by date
        """
        date_filter_lte = request.data.get('date_filter_lte', '2999-12-31')
        date_filter_gte = request.data.get('date_filter_gte', '1970-01-01')
        statistic = CurrencyRates.objects. \
            filter(day_of_rate__range=[date_filter_gte, date_filter_lte]).values('to_currency') \
            .annotate(min=Min('sale_rate'), max=Max('sale_rate'))
        logger.debug(f'User: {request.user} get response {statistic}')
        return Response({'statistics': statistic})


class UsersExchangeOperationsView(mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin,
                                  mixins.ListModelMixin,
                                  GenericViewSet):
    """
    View for creating, deleting, getting users currency operations
    """

    permission_classes = [IsAuthenticated]
    serializer_class = GetUsersExchangeOperationsSerializer

    def perform_create(self, serializer):
        """
        Called by CreateModelMixin when saving a new object instance.
        :param serializer: serializer
        :return:
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Returns the queryset that should be used for list views,
        and that should be used as the base for lookups in detail views.
        :return:
        """
        return (UsersExchangeOperations.objects
                .filter(user=self.request.user.id)
                .annotate(amount_operation=models.F('count') * models.F('currency__sale_rate'))
                .select_related('user', 'currency')
                )


class UserRegistrationView(mixins.CreateModelMixin,
                           GenericViewSet):
    """
    View for creating user
    """
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    View for updating or retrieving user
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'username'


class APIChangePasswordView(generics.UpdateAPIView):
    """
    View for updating password
    """

    serializer_class = UserPasswordChangeSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get_object(self, queryset=None):
        logger.debug(f'User: {self.request.user} get response by url {self.request.get_full_path()}')
        return self.request.user


def auth(request):
    return render(request, 'oauth.html')