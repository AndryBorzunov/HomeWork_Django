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

from catalog.models import Product


class ProductListView(ListView):
    model = Product


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
        if user == self.object.owner or user.has_perm("catalog.can_delete_product"):
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
