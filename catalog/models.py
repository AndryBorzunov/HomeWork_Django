from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=64,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    description = models.TextField(
        verbose_name="Описание  категории", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=64, verbose_name="Наименование", help_text="Введите наименование"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Описание продукта"
    )
    photo = models.ImageField(
        upload_to="products/photo", verbose_name="Фото", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Выберите категорию продукта",
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену за покупку")
    created_at = models.DateField(verbose_name="Дата создания")
    updated_at = models.DateField(verbose_name="Дата последнего изменения")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца продукта",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_published = models.BooleanField(verbose_name="Признак публикации", default=False)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["category", "name"]
        permissions = [
            ("can_unpublish_product", "can unpublish product"),
        ]

    def __str__(self):
        return self.name
