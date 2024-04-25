from rest_framework.fields import empty
from alinaverenaapi.models import *
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField


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

    return len(client) > 0, ipaddress, client


class ArticleSerializer(TranslatableModelSerializer):
    article_text = TranslatedFieldsField(shared_model=Article)
    is_favorite = serializers.SerializerMethodField('is_user_favorite_article')

    def is_user_favorite_article(self, obj: Article):
        request = self.context.get("request")

        if request.user.is_anonymous:
            exists, ipaddress, client = check_client_exists(request)

            if exists:
                return len(Article.objects.filter(favorite__id=client.first().id)) > 0

        return Article.objects.filter(favorite__id=request.user.id)

    class Meta:
        model = Article
        fields = ('id', 'image_desktop', 'is_favorite', 'image_responsive',
                  'article_text', 'active', 'article_text', 'collection')


class ProductSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField()
    category = serializers.SlugRelatedField('category_name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['belonging_feature', 'product_image']


class CompleteProductSerializer(serializers.Serializer):
    product = ProductSerializer()
    images = ProductImagesSerializer(many=True)
    colors = serializers.JSONField()
    features = serializers.JSONField()
    images_by_features = serializers.JSONField()


class FrontendLoadingBackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrontendLoadingBackgroundImage
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone_number',
                  'email', 'country', 'language', 'currency', 'password']


class ClientFrontendInformation(serializers.Serializer):
    pass


class PurchaseOrderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        purchase = Purchase.objects.create(**validated_data)
        ip = get_client_ip(self.context['request'])
        if self.instance is not None:
            client = Client.objects.filter(user_ipaddress=ip)
            anon_client = AnonymousClient.objects.filter(user_ipaddress=ip)
            if len(client):
                purchase.purchase_client = client.first()
            elif len(anon_client):
                purchase.purchase_anon_client = anon_client.first()
        return purchase

    class Meta:
        model = Purchase
        fields = ['firstName', 'lastName', 'email',
                  'phoneNumber', 'productId', 'purchaseInfo', 'price', 'currency']
