import os
from alinaverenaapi.models import ProductCategory, Product, ProductImage, Client
from django.contrib.auth import get_user_model
from django.core.files import File

User = get_user_model()
User.objects.create_superuser(email="alaoui197011@gmail.com", password="Uhphamza12,",
                              first_name="Hamza", last_name="Alaoui", phone_number="+212627755969")

category = ProductCategory(category_name="heels").save()
product = Product()

product.set_current_language("en")
product.title = "Sole Elegance: A Stiletto Story"
product.description = "Step into sophistication with our latest heels collection, where every pair tells a story of elegance and allure. From classic pumps to trendy platforms, our curated selection offers the perfect blend of style and comfort to elevate any ensemble. Whether you're strutting into the boardroom or dancing the night away, our heels collection ensures you'll make a statement with every step. Indulge in luxurious materials, exquisite craftsmanship, and versatile designs that effortlessly transition from day to night. Embrace your inner confidence and exude timeless charm with our meticulously curated heels collection."

product.features = [
    {"value": "Black color."},
    {"value": "Pure natural cuir."},
    {"value": "Sharp heels."},
    {"value": "33 mm heel."},
]

product.set_current_language("ru")
product.title = "Изысканная подошва: История стилетов"
product.description = "Войдите в мир утонченности с нашей последней коллекцией каблуков, где каждая пара рассказывает историю элегантности и очарования. От классических туфель до трендовых платформ, наша отобранная подборка предлагает идеальное сочетание стиля и комфорта, чтобы поднять любой наряд на новый уровень. Будь то выход в офис или танцы до утра, наша коллекция каблуков обеспечивает выразительность с каждым шагом. Наслаждайтесь роскошными материалами, изысканным мастерством и универсальными дизайнами."
product.features = [
    {"value": "Black color."},
    {"value": "Pure natural cuir."},
    {"value": "Sharp heels."},
    {"value": "33 mm heel."},
]
product.category = category
product.price = 79.99
product.privilege = True
product.product_color = "#E1AFD1"
product.is_product_color_dark = False
product.quantities = [{"other": {"size": 36, "color": "#E1AFD1"}, "availableQuantity": 200}, {"other": {
    "size": 37, "color": "#E1AFD1"}, "availableQuantity": 300}, {"other": {"size": 38, "color": "#E1AFD1"}, "availableQuantity": 300},
    {"other": {"size": 36, "color": "white"}, "availableQuantity": 300},
    {"other": {"size": 37, "color": "white"}, "availableQuantity": 200},
    {"other": {"size": 38, "color": "white"}, "availableQuantity": 800},
    {"other": {"size": 39, "color": "white"}, "availableQuantity": 400}
]
product.save()

files_paths = [
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_1_1.jpg", "color": "#E1AFD1"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_2_1.jpg", "color": "#E1AFD1"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_3_1.jpg", "color": "#E1AFD1"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_4_1.jpg", "color": "#E1AFD1"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_1_1.jpg", "color": "white"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_2_1.jpg", "color": "white"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_3_1.jpg", "color": "white"},
    {"path": "/Users/hamzaalaouy/Downloads/1000210800_6_4_1.jpg", "color": "white"},
]

for image_path in files_paths:
    with open(image_path["path"], 'rb') as image_file:
        django_file = File(image_file)
        filename = os.path.basename(image_path["path"])
        image = ProductImage(product_base=product,
                             belonging_feature={"color": image_path["color"]})

        image.product_image.save(filename, django_file)