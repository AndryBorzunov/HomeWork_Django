from unicodedata import category

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from catalog.forms import ProductForm, ProductModeratorForm

from catalog.models import Product, Category
from catalog.services import get_products_from_cache, get_products_by_category


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        categories = Category.objects.all()
        products = get_products_from_cache()
        context = { 'products_category': categories, 'object_list': products}
        return context


class ProductByCategoryListView(ListView):
    model = Product

    categories = Category.objects.all()
    context = { 'products_category': categories, }

    def get_context_data(self, *args, **kwargs):
        categories = Category.objects.all()
        category_id = self.kwargs.get('category_id')
        products = get_products_by_category(category_id)
        context = { 'products_category': categories, 'object_list': products}
        return context

    #def get_queryset(self):
    #    category_id = self.kwargs.get('category_id')
    #    return get_products_by_category(category_id)


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.owner or user.has_perm("catalog.delete_product"):
            return super().form_valid(form)
        raise PermissionDenied


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"
    context_object_name = "catalog:contacts"
    # fields = ("name", "phone", "message")
    # success_url = reverse_lazy('catalog:products_list')


# def contacts(request):
#    if request.method == "POST":
#        name = request.POST.get("name")
#        message = request.POST.get("message")
#        print(name)
#        print(message)
#        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
#    return render(request, "contacts.html")
