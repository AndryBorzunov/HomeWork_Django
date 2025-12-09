from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, products_list, product_detail

app_name = CatalogConfig.name

urlpatterns = [
    path("", products_list, name="products_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("contacts/", contacts, name="contacts"),
]
