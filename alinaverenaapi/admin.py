from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm
from django.utils.translation import gettext as _
from parler.admin import TranslatableAdmin
from .models import *


@admin.register(Client)
class ClientAdmin(UserAdmin):
    form = UserChangeForm
    fieldsets = [
        (
            _("Credentials"),
            {
                "fields": ['first_name', 'last_name', 'email', 'phone_number', 'user_ipaddress'],
                "classes": "wide"
            }
        ),
        (
            _("Permissions"),
            {
                "fields": ["is_active", "is_staff", "is_superuser", "user_permissions"],
                "classes": "wide"
            }
        ),
        (
            _("Account activity"),
            {
                "fields": ["date_joined", "last_login"],
            }
        ),
        (
            _("Client information's"),
            {
                "fields": ["language", "country", 'currency']
            }
        )
    ]

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    exclude = ['username']
    list_display = ['user_ipaddress', "first_name", "last_name", 'email']
    search_fields = ["email", "first_name", "last_name",
                     "phone_number", "country", "language"]
    ordering = ['email', ]


@admin.register(AnonymousClient)
class AnonymousClient(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": ["user_ipaddress"]
        }),
    )


@admin.register(Article)
class ArticleAdmin(TranslatableAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'active']
    fieldsets = [
        (
            _("Article images"),
            {
                "fields": ['image_desktop', 'image_responsive', 'image_dark_mode'],
                "classes": "wide"
            }
        ),
        (
            _("Article text"),
            {
                "fields": ['title', 'description'],
                "classes": "wide"
            }
        ),
        (
            _("Client favorite article"),
            {
                "fields": ['favorite'],
                "classes": "wide"
            }
        ),
        (
            _("Visibility of article"),
            {
                "fields": ['active'],
                "classes": "wide"
            }
        ),
        (
            _("Products in article"),
            {
                "fields": ['collection'],
                "classes": "wide"
            }
        )
    ]


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ['name', 'category', 'products_in_article'],
        }),
    ]

    search_fields = ['name']
    ordering = ['name']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Category", {
            "fields": ['category_name']
        })
    ]

    search_fields = ['category_name']
    ordering = ['category_name']


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    fieldsets = [
        ("Product basic information's", {
            "fields": ['title', 'description', 'features', 'price', 'category', 'privilege', 'date_added',
                       'product_color', 'is_product_color_dark'],
            "classes": ['wide']
        }),
        ("Quantity", {
            "fields": ['quantities'],
            "classes": ['wide']
        }),
    ]

    readonly_fields = ['date_added']

    search_fields = ['title', 'features', 'quantities', 'identifier_link']


@admin.register(ProductImage)
class ProductImagesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ['belonging_feature', 'product_base', 'product_image']
        })
    ]


@admin.register(FrontendLoadingBackgroundImage)
class FrontendLoadingBackgroundImageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ["image_desktop", "image_phone", "dark_image", "active"]
        })
    ]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            "fields": ['purchase_client', 'purchase_anon_client', 'firstName', 'lastName', 'email', 'price', 'phoneNumber', 'productId', 'purchaseInfo', 'currency']
        })
    ]
