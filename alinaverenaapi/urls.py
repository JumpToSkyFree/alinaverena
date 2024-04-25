from alinaverenabackend import settings
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'alinaverenaapi'

urlpatterns = [
    path('articles/', ArticleView.as_view(), name='articles'),
    path('products/category/<category>',
         ProductsByCategoryView.as_view(), name='products'),
    path('products/category/<category>/<current_page>',
         ProductsByCategoryView.as_view(), name='products'),
    path('privilege-products',
         PrivilegeProducts.as_view(), name='privilege-products'),
    path('products/', ProductsView.as_view(), name='products'),
    path('home-products/', HomeProductsView.as_view(), name='home-products'),
    path('product/<pk>', ProductView.as_view(), name='product'),
    path('user-information/', ProductView.as_view(), name='user-information'),
    path('page-loading-image', FrontendLoadingBackgroundImageViewset.as_view(),
         name="page-loading-image"),
    path('client/register', ClientRegister.as_view(), name="client-register"),
    path('client/login', ClientLogin.as_view(), name="client-login"),
    path('client/access', ClientAccessTest.as_view()),
    path('available-languages/', AvailableBackendLanguages.as_view(),
         name="available-languages/"),
    path('purchase-order', PurchaseOrder.as_view(), name='purchase-order')
]
