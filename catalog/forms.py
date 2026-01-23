from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product
from config.settings import FORBIDDEN_WORDS, MAX_SIZE


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                #field.widget.attrs.update({'class': 'form-check'})
                field.widget.attrs['class'] = 'form-check-input'
                #field.widget.attrs['input type'] = 'checkbox'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Product
        exclude = ("owner", "is_published",)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise ValidationError("Запрещенное слово в названии")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise ValidationError("Запрещенное слово в описании")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной")
        return price

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")

        if photo is not None:
            if photo.size > 1024 * 1024 * MAX_SIZE:
                raise ValidationError(f"Размер фото превышает {MAX_SIZE} Мб")

            content_type = photo.content_type
            if content_type not in ("image/jpeg", "image/webp", "image/png"):
                raise ValidationError(
                    f"Формат файла не соответствует формату изображения {content_type}"
                )

        return photo


class ProductModeratorForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Product
        fields = ("is_published",)
