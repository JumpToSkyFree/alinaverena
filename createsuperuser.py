import os
from alinaverenaapi.models import ProductCategory, Product, ProductImage, Client
from django.contrib.auth import get_user_model
from django.core.files import File

User = get_user_model()
User.objects.create_superuser(email="alaoui197011@gmail.com", password="Uhphamza12,",
                              first_name="Hamza", last_name="Alaoui", phone_number="+212627755969")