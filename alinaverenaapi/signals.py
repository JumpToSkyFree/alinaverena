import datetime
import pickle
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product, ProductImage, Client, Purchase
from rest_framework.authtoken.models import Token
from alinaverenaapi import loop, send_message
from .views import get_all_features_of_product, get_all_colors_of_product, get_all_images_by_features_values
from django.conf import settings


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

@receiver([pre_delete], sender=ProductImage)
def delete_product_image_media(sender, instance: ProductImage, **kwargs):
    if instance.product_image:
        instance.product_image.delete(False)

@receiver([post_save], sender=Product)
def save_product_images_features_from_product(sender, instance, **kwargs):
    product_images = ProductImage.objects.filter(
        product_base=instance.id)

    images_by_features = pickle.dumps(get_all_images_by_features_values(
        product_images=product_images))
    features = pickle.dumps(get_all_features_of_product(
        product_images=product_images))
    colors = pickle.dumps(get_all_colors_of_product(
        product_images=product_images))

    cache.set('product-' + instance.id.__str__() +
              '-images-by-features', images_by_features, None)
    cache.set('product-' + instance.id.__str__() +
              '-features', features, None)
    cache.set('product-' + instance.id.__str__() +
              '-colors', colors, None)



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


@receiver([post_save], sender=Purchase)
def notify_purcahse_made(sender, instance: Purchase | None=None, created=False, **kwargs):
    if created and instance is not None:
        if instance.lastName != "":
            if not settings.DEBUG:
                loop.run_until_complete(send_message(f"A new purchase is made by {instance.firstName} {instance.lastName}, bought {instance.productId}, i love you my cat."))
                return

        loop.run_until_complete(send_message(f"A new purchase is made by {instance.firstName} and email {instance.phoneNumber}, bought {instance.productId}, i love you my cat."))


@receiver([pre_delete], sender=Purchase)
def notify_purcahse_deleted(sender, instance: Purchase | None=None, **kwargs):
    if instance is not None:
        if not settings.DEBUG:
            loop.run_until_complete(send_message(f"Purchase of {instance.firstName} {instance.lastName} is done."))