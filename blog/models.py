from django.db import models


class Article(models.Model):
    heading = models.CharField(
        max_length=64,
        verbose_name="Заголовок",
        help_text="Введите заголовок"
    )

    content = models.TextField(
        verbose_name="Содержание",
        help_text="Содержание статьи"
    )

    preview = models.ImageField(upload_to="articles/photo", blank=True, null=True)

    created_at = models.DateField(verbose_name="Дата создания", auto_now=True)

    is_published = models.BooleanField(verbose_name="Признак публикации", default=False)

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0
    )

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.heading
