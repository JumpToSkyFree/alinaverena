import json
import os

from django.views.generic import TemplateView

# from django.utils.decorators import method_decorator
from alinaverenabackend.settings import PARLER_LANGUAGES, CURRENCIES_FILE_PATH, SITE_ID
import requests
import pickle
from .modelfields import Languages
from django.views.decorators.cache import cache_page
from django.views import View
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.request import Request
from django.conf import settings
from django.core.cache import cache
from alinaverenaapi.models import Article, Product, ProductImage
from alinaverenaapi.serializers import *
import decimal
from .models import Client, FrontendLoadingBackgroundImage
from .serializers import FrontendLoadingBackgroundImageSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


class ArticleView(APIView):
    def get_object(self):
        articles = Article.objects.filter(active=True)
        return articles

    def get(self, request):
        articles: Article = self.get_object()
        articles_serializer = ArticleSerializer(articles, many=True, context={
            'request': request
        })

        return Response(articles_serializer.data)


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_client_exists(request):
    ipaddress = get_client_ip(request)

    if ipaddress is None:
        return ipaddress

    client = Client.objects.filter(user_ipaddress=ipaddress)

    return client is not None, ipaddress, client


def register_new_guest_client_and_get(request, currency, language, country):
    exists, ipaddress, client = check_client_exists(request)
    client = None

    if not exists:
        _client = Client(user_ipaddress=ipaddress,
                         language=language, country=country, currency=currency)
        _client.save()
        return _client

    return client


def get_all_features_of_product(product_images):
    features = set()

    for product_image in product_images:
        for feature, _ in product_image.belonging_feature.items():
            features.add(feature)

    return features


def get_all_images_by_features_values(product_images):
    """
    {
        'color': [
            'value': '#000000',
            'images': [
                'https....',
                'https....',
                'https....'
            ]
        ],
    }
    """

    product_features = get_all_features_of_product(
        product_images=product_images)
    images_by_features = dict()

    # TODO: Arrange all images by features, not working well, fix it.

    def get_all_values_of_feature(__product_images, _feature):
        _values_of_feature = []
        for _product_image in __product_images:
            try:
                _values_of_feature.append(
                    _product_image.belonging_feature[_feature])
            except KeyError:
                pass

        return _values_of_feature

    for feature in product_features:
        values_of_feature = get_all_values_of_feature(product_images, feature)
        images_by_features[feature] = []
        for value in values_of_feature:
            exists = False
            # if value not in images_by_features[feature]:
            for _value in images_by_features[feature]:
                if _value['value'] == value:
                    exists = True
                    break

            if not exists:
                images_by_features[feature].append({
                    'value': value,
                    'images': []
                })

    for feature in product_features:
        for product_image in product_images:
            if feature in product_image.belonging_feature:
                index = 0
                for _feature in images_by_features[feature]:
                    if _feature.get('value') == product_image.belonging_feature[feature]:
                        images_by_features[feature][index]['images'].append(
                            product_image.product_image.url)
                    index += 1

    return images_by_features


def set_currency_exchange() -> None:
    def should_update_currencies_exchange_rate() -> bool:
        # TODO: Change days from 1 to 30.
        if cache.get('currency_last_update') is None or (datetime.now() - cache.get('currency_last_update')).days >= 1:
            cache.set('currency_last_update', datetime.now())
            return True

        return False

    if should_update_currencies_exchange_rate():
        exchange_rate_data = requests.get(
            'https://api.currencyapi.com/v3/latest?apikey=cur_live_0ixbsWwBQLmWTLNS6OmUrpQzBZq0yyloUXgoD49L')
        cache.set('exchange_rate', exchange_rate_data.json())

    return cache.get('currency_last_update')


def get_product_images_as_object(product: str | Product | None, request):
    def build_url_images_as_object(ibf: dict):
        for feature_name, _ in ibf.items():
            for index, feature_list in enumerate(ibf.get(feature_name)):
                for img_it in range(len(ibf.get(feature_name)[index].get('images'))):
                    ibf.get(feature_name)[index].get('images')[img_it] = request.build_absolute_uri(
                        ibf.get(feature_name)[index].get('images')[img_it])
        return ibf

    product_images = ProductImage.objects.filter(product_base=product)

    images_by_features = cache.get(
        'product-' + product.id.__str__() + '-images-by-features')
    # images_by_features = pickle.loads(cache.get('product-' + product.identifier_link + '-images-by-features'))
    features = cache.get('product-' + product.id.__str__() + '-features')
    colors = cache.get('product-' + product.id.__str__() + '-colors')

    if (images_by_features and features and colors) is not None:
        images_by_features = build_url_images_as_object(
            pickle.loads(images_by_features))
        # images_by_features = pickle.loads(cache.get('product-' + product.identifier_link + '-images-by-features'))
        features = pickle.loads(features)
        colors = pickle.loads(colors)

    return {
        'product': product,
        'images': product_images,
        'colors': colors,
        'features': features,
        'images_by_features': images_by_features
    }


def set_product_object_currency_price(product, currency) -> list | None:
    data = cache.get('exchange_rate')

    if data is not None:
        currency_data = None

        if data.get('data') is not None:
            currency_data = data.get('data').get(currency)

        if currency_data is None:
            return product

        if product is not None:
            product['product'].price = product['product'].price * \
                decimal.Decimal(currency_data.get('value'))

    product['currency'] = currency

    return product


def get_all_colors_of_product(product_images):
    colors = set()

    for product_image in product_images:
        try:
            colors.add(product_image.belonging_feature['color'])
        except KeyError:
            pass

    return colors


class ProductsByCategoryView(APIView):
    # pagination_class = settings.DEFAULT_PAGINATION_CLASS

    @staticmethod
    def get_products(category: str | None):
        if category is None:
            return Product.objects.all()

        products_of_category = Product.objects.filter(
            category__category_name=category)

        return products_of_category

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, category: str | None, current_page: int | None):
        products = []
        currency = request.query_params.get('currency')

        if currency is None:
            currency = "USD"

        set_currency_exchange()

        for product in self.get_products(category=category):
            products.append(get_product_images_as_object(
                product=product, request=request))

        for index, product in enumerate(products):
            products[index] = set_product_object_currency_price(
                product, currency)

        page = Paginator(products, 9)

        result_page = products

        try:
            if page is not None:
                result_page = page.page(int(current_page) + 1)
        except EmptyPage:
            return Response({"message": "page contains no results", "code": "page-contains-no-results"})

        product_serializer = CompleteProductSerializer(result_page, many=True, context={
            'request': request
        })

        return Response({
            'page_result': product_serializer.data,
            'page_data': {
                'count': page.count,
                'num_pages': page.num_pages,
            }
        })

    # @property
    # def paginator(self):
    #     if self.pagination_class is None:
    #         self._paginator = None

    #     else:
    #         self._paginator = self.pagination_class()

    #     return self._paginator

    # def paginate_queryset(self, queryset):
    #     if self.paginator is None:
    #         return None

    #     return self.paginator.paginate_queryset(queryset, self.request, view=self)

    # def get_paginated_response(self, data):
    #     assert self.paginator is not None
    #     return self.paginator.get_paginated_response(data)


class PrivilegeProducts(APIView):
    # pagination_class = settings.DEFAULT_PAGINATION_CLASS

    @staticmethod
    def get_products():
        privilege_products = Product.objects.filter(
            privilege=True)

        return privilege_products

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        products = []
        currency = request.query_params.get('currency')

        if currency is None:
            currency = "USD"

        set_currency_exchange()

        for product in self.get_products():
            products.append(get_product_images_as_object(
                product=product, request=request))

        for index, product in enumerate(products):
            products[index] = set_product_object_currency_price(
                product, currency)

        product_serializer = CompleteProductSerializer(products, many=True, context={
            'request': request
        })

        return Response(product_serializer.data)


class ProductsView(APIView):
    @staticmethod
    def get_products():
        products_of_category = Product.objects.all()

        return products_of_category

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        products = []
        currency = request.query_params.get('currency')

        if currency is None:
            currency = "USD"

        set_currency_exchange()

        for product in self.get_products():
            products.append(get_product_images_as_object(
                product=product, request=request))

        for index, product in enumerate(products):
            products[index] = set_product_object_currency_price(
                product, currency)

        product_serializer = CompleteProductSerializer(
            products, many=True, context={
                'request': request
            })

        return Response(product_serializer.data)


class HomeProductsView(APIView):
    @staticmethod
    def get_products():
        products_of_category = Product.objects.filter(privilege=True)

        return products_of_category

    # @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        products = []
        currency = request.query_params.get('currency')

        if currency is None:
            currency = "USD"

        set_currency_exchange()

        for product in self.get_products():
            products.append(get_product_images_as_object(
                product=product, request=request))

        for index, product in enumerate(products):
            products[index] = set_product_object_currency_price(
                product, currency)

        product_serializer = CompleteProductSerializer(
            products, many=True, context={
                'request': request
            })

        return Response(product_serializer.data)


class ProductView(APIView):
    @staticmethod
    def get_product_by_identifier(pk: str):
        product = Product.objects.filter(
            id=pk).first()

        return product

    def get(self, request: Request, pk):
        currency = request.query_params.get('currency')

        if currency is None:
            currency = "USD"

        product_obj = self.get_product_by_identifier(pk=pk)

        if product_obj is None:
            return Response({
                'message': 'Not Found'
            })

        product = get_product_images_as_object(
            product_obj, request=request)

        set_currency_exchange()

        product = set_product_object_currency_price(product, currency)

        product_serializer = CompleteProductSerializer(
            product, context={
                'request': request
            })

        return Response(product_serializer.data)


class FrontendLoadingBackgroundImageViewset(APIView):
    def get(self, request):
        queryset = FrontendLoadingBackgroundImage.objects.filter(active=True)
        serializer = FrontendLoadingBackgroundImageSerializer(queryset.first(), context={
            'request': request
        })
        return Response(serializer.data)


class ClientLogin(APIView):
    def get(self, request):

        client = get_object_or_404(Client, email=request.data['email'])

        if not client.check_password(request.data['password']):
            return Response({"detail": "Not found."}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=client)
        serializer = ClientSerializer(instance=client)
        return Response({"token": token.key, "client": serializer.data})


class ClientRegister(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.user_ip_address = get_client_ip(request)
            serializer.last_visit = datetime.now()
            serializer.save()
            client = Client.objects.filter(email=request.data['email']).first()
            client.set_password(request.data['password'])
            client.save()

            token, created = Token.objects.get_or_create(user=client)

            return Response({"token": token.key, "user": serializer.data, "success": True})

        return Response({"errors": serializer.errors, "success": False}, status=status.HTTP_400_BAD_REQUEST)


class ClientAccessTest(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request):
        return Response("passed for {}".format(request.user.email))


class AvailableBackendLanguages(APIView):
    def get(self, value):
        # Get the available languages from the settings
        codes = [
            {'code': language['code']}
            for language in PARLER_LANGUAGES.get(SITE_ID)
        ]

        try:
            # TODO: Add languages sources json file from settings.
            langs = Languages(os.path.join(os.path.join(
                os.getcwd(), CURRENCIES_FILE_PATH), 'languages.json'))
        except Exception as e:
            return Response({'error': e.message})

        for code in codes:
            code['info'] = langs.get_language_by_code(code.get('code'))

        return Response(codes)


class PurchaseOrder(APIView):
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data, context={
            'request': request
        })


        if serializer.is_valid():
            serializer.save()
            return Response({"message": "order successful."})


        errors = dict()

        try:
            for name, _ in serializer.errors.items():
                errors[name] = [
                    error.code for error in serializer.errors[name]
                ]
        except Exception as e:
            print(e)

        return Response(errors, status=status.HTTP_200_OK)


class ReactRoute(TemplateView):
    template_name = "index.html"
