from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from catalog.forms import ProductForm

from catalog.models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products_list")


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
