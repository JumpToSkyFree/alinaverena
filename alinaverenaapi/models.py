from collections.abc import Iterable
from typing import Any
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from .modelfields import CountryField, LanguageField, CurrencyField
from django.utils.translation import gettext as _
from parler.models import TranslatableModel, TranslatedFields
from phonenumber_field.modelfields import PhoneNumberField
import datetime


class ClientUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required to create a user.")

        if not password:
            raise ValueError("Password is required to create a user.")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault(
            'phone_number', extra_fields.get('phone_number'))
        extra_fields.setdefault('last_visit', datetime.datetime.now())

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('last_visit', datetime.datetime.now())

        superuser = self._create_user(email, password, **extra_fields)
        superuser.is_admin = True
        return superuser


class Client(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    country = CountryField(default='US', null=False)
    language = LanguageField(default='en', null=False)
    currency = CurrencyField(default='USD')
    last_visit = models.DateTimeField(blank=True, null=True)
    user_ipaddress = models.GenericIPAddressField(
        max_length=46, blank=False, default="127.0.0.1")
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)

    username = None

    def __str__(self):
        return self.first_name + " " + self.last_name

    objects = ClientUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'phone_number', 'password']


class AnonymousClient(models.Model):
    user_ipaddress = models.GenericIPAddressField(
        max_length=46, blank=False, default="127.0.0.1")


class ProductCategory(models.Model):
    category_name = models.CharField(
        _("Category"), max_length=128, blank=False, unique=True)

    def save(self, *args, **kwargs) -> None:
        self.category_name = self.category_name.lower()
        return super().save()

    def __str__(self) -> str:
        return self.category_name

    class Meta:
        verbose_name_plural = 'Product Categories'


class Product(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=128,
                               blank=False, unique=True),
        description=models.TextField(_("Description"), blank=False),
        features=models.JSONField(_("Features"))
    )

    privilege = models.BooleanField(default=False)

    """
    {
       availableQuantity: 300,
       other: {
           size: 38,
           color: 'black'
       }
    },
    {
       availableQuantity: 300,
       other: {
           size: 38,
           color: 'black'
       }
    }

    type Quantity = {
        availableQuantity: number,
        other: any, { 'size', 'color' }
    }

    type quantities = Array<Quantity>;
    """

    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, null=True)
    quantities = models.JSONField(
        verbose_name=_("Quantity of each wearable size"))

    # TODO: Make a future price field that calculates rate change of other currencies.
    price = models.DecimalField(verbose_name=_(
        "Price"), max_digits=16, decimal_places=2)

    date_added = models.DateTimeField(
        _("Time Added"), auto_now=True, auto_now_add=False, null=True)

    product_color = models.CharField(
        verbose_name=_("Product color"), max_length=128, blank=False, default="#000000")

    is_product_color_dark = models.BooleanField(
        verbose_name=_("is product color dark"), default=False
    )

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    """
    type belongingFeature = {
        color: string
    }
    """
    belonging_feature = models.JSONField(verbose_name=_("Belonging feature"))
    product_base = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_image = models.ImageField(verbose_name=_("Product image"))

    def __str__(self):
        return f'{self.product_base.title} image'


class ProductCollection(models.Model):
    name = models.CharField(_("Collection name"),
                            max_length=50, blank=True)
    category = models.ForeignKey(
        ProductCategory, verbose_name=_("Collection Category"), on_delete=models.CASCADE)
    products_in_article = models.ManyToManyField(
        Product, verbose_name=_("Heels in article"), blank=True)


class Article(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_desktop = models.ImageField(
        _("Article image for desktop"), upload_to="article-images/%Y/%M/%D/", blank=False)
    image_responsive = models.ImageField(
        _("Article image responsive"), upload_to="article-images-responsive/%Y/%M/%D/", blank=False)
    image_dark_mode = models.BooleanField(_("Image dark mode"), default=False)

    article_text = TranslatedFields(
        title=models.CharField(
            _("Article title"), max_length=64, blank=False, unique=True),
        description=models.TextField(_("Article description"), blank=False)
    )
    favorite = models.ManyToManyField(
        to=Client, verbose_name=_("Clients favorite articles."), blank=True)
    active = models.BooleanField(_("Visible active"), default=False)
    collection = models.ForeignKey(
        ProductCollection, verbose_name=_("Product Collection"), on_delete=models.CASCADE, blank=True, null=True)


class FrontendLoadingBackgroundImage(models.Model):
    image_desktop = models.ImageField(
        _("Loading background image for desktop"), upload_to="loading-images/%Y/%M/%D/", blank=False)
    image_phone = models.ImageField(
        _("Loading background image for phone"), upload_to="loading-images/%Y/%M/%D/", blank=False)
    dark_image = models.BooleanField(_("Is picture dark?"), blank=False)
    active = models.BooleanField(
        _("Active image in the website?"), default=True)

    def save(self, *args, **kwargs):
        FrontendLoadingBackgroundImage.objects.filter(
            active=True).update(active=False)
        return super().save(*args, **kwargs)


class Purchase(models.Model):
    purchase_client = models.ForeignKey(
        to=Client, on_delete=models.CASCADE, blank=True, null=True)
    purchase_anon_client = models.ForeignKey(
        to=AnonymousClient, on_delete=models.CASCADE, blank=True, null=True)

    firstName = models.CharField(_("first name"), max_length=150, blank=False)
    lastName = models.CharField(
        _("last name"), max_length=150, blank=True, null=True)
    email = models.EmailField(blank=False, null=True)
    price = models.DecimalField(verbose_name=_(
        "Price"), max_digits=16, decimal_places=2, blank=False, null=True, default=79.99)
    phoneNumber = PhoneNumberField(blank=False, null=False, unique=False)
    productId = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    currency = CurrencyField(default='USD')

    purchaseInfo = models.JSONField(_("Purchase info"))