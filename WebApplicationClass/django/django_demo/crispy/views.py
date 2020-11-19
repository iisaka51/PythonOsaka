from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    fields = ('name', 'email')
    template_name = 'crispy_product_list.html'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'crispy_product.html'
    success_url = reverse_lazy('crispy:product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'crispy_product_update.html'
    success_url = reverse_lazy('crispy:product_list')
