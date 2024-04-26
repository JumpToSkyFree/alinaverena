import datetime
import pickle
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, ProductImage, Client
from rest_framework.authtoken.models import Token
from .views import get_all_features_of_product, get_all_colors_of_product, get_all_images_by_features_values


@receiver([post_save, post_delete], sender=ProductImage)
def save_product_images_features(sender, instance: ProductImage, **kwargs):
    product_images = ProductImage.objects.filter(
        product_base=instance.product_base)

    images_by_features = pickle.dumps(get_all_images_by_features_values(
        product_images=product_images))
    features = pickle.dumps(get_all_features_of_product(
        product_images=product_images))
    colors = pickle.dumps(get_all_colors_of_product(
        product_images=product_images))

    cache.set('product-' + instance.product_base.id.__str__() +
              '-images-by-features', images_by_features, None)
    cache.set('product-' + instance.product_base.id.__str__() +
              '-features', features, None)
    cache.set('product-' + instance.product_base.id.__str__() +
              '-colors', colors, None)


# @receiver([post_save], sender=Product)
# def save_product_images_features(sender, instance, **kwargs):
#     if cache.get('product-' + instance.id.__str__() + 'images_by_features') is None:
#         pass


@receiver([post_save, post_delete], sender=Product)
def invalidate_signal_product_image(sender, instance, **kwargs):
    pass


@receiver([pre_save], sender=Client)
def notify_user_access(sender, instance: Client, created=False, **kwargs):
    instance.last_visit = datetime.datetime.now()


@receiver([post_save], sender=Client)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)