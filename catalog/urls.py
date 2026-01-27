from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductByCategoryListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ContactsView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path("products/category/<int:category_id>/", ProductByCategoryListView.as_view(), name="products_category_list"),
    path("products/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="products_create"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="products_update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="products_delete"
    ),
    path(
        "contacts/",
        ContactsView.as_view(template_name="catalog/contacts.html"),
        name="contacts",
    ),
]
