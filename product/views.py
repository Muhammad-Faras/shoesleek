from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.urls import reverse
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import *
from .forms import *

class ProductCategoryView(ListView):
    model = SubCategoryModel
    template_name = 'product/product_category.html'  # Specify your template name
    context_object_name = 'subcategories'

    def get_queryset(self):
        self.main_category = get_object_or_404(MainCategoryModel, main_category_name=self.kwargs['category_name'])        
        return SubCategoryModel.objects.filter(main_category=self.main_category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_category'] = self.main_category 
        return context
    
    
        
class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'  # Template for displaying products
    context_object_name = 'products_list'

    def get_queryset(self):
        subcategory_name = self.kwargs.get('subcategory_name')
        self.subcategory = get_object_or_404(SubCategoryModel, sub_category_name=subcategory_name)
        return Product.objects.filter(sub_category=self.subcategory)
    
    

class ProductDetailView(DetailView):
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    model = Shoe
    def get_object(self, queryset=None):
        product_type = self.kwargs.get('product_type')  # Get the captured product_type from URL
        pk = self.kwargs.get('pk')  # Get the captured pk (primary key) from URL
        
        print('------------',pk,'------------')
        print('------------',product_type,'------------')
        
        # # Determine the model based on the product_type
        # if product_type == 'Shoes':
        #     self.model = Shoe
        
        # else:
        #     self.model = Product
        
        # Fetch the specific product instance using get_object_or_404
        return get_object_or_404(self.model, pk=pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["product_type"] = self.kwargs.get('product_type') 
        context['form'] = AddToCartForm(initial={'product_id': self.object.id})
        if isinstance(product, Shoe):
            # Get all other shoe objects except the current one
            other_shoes = Shoe.objects.filter(sub_category=product.sub_category).exclude(pk=product.pk)
            for i in other_shoes:
                print('-----------',i,'--------------')
            context['other_shoes'] = other_shoes

        return context
    


class AddToCartView(LoginRequiredMixin,TemplateView):
    template_name = 'product/product_cart.html'

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            product = get_object_or_404(Product, id=product_id)
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
        return redirect('product:product_cart')

class ProductCartView(LoginRequiredMixin, TemplateView):
    template_name = 'product/product_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total_price = sum(item.quantity * item.product.price for item in cart_items)
        shipping = 10
        total_price = sub_total_price + shipping
    # Add cart items and total price to the context
        context['sub_total_price'] = sub_total_price
        context['total_price'] = total_price
        context['shipping'] = shipping
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        
        return context


# class ProductDetailView(TemplateView):
#     template_name = 'product/product_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         product_type = self.kwargs.get('product_type')
#         pk = self.kwargs.get('pk')

#         if product_type == 'laptop':
#             product = get_object_or_404(Laptop, pk=pk)
#         else:
#             product = get_object_or_404(Product, pk=pk)

#         context['product'] = product
#         return context
    
   
    

# class ProductCartView(TemplateView):
#     template_name = 'product/product_cart.html'

def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('product:product_cart')  # Redirect to the cart page after removal

class CheckoutView(LoginRequiredMixin ,TemplateView):
    template_name = 'product/payment_checkout.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        sub_total_price = sum(item.quantity * item.product.price for item in cart_items)
        shipping = 10
        total_price = sub_total_price + shipping
    # Add cart items and total price to the context
        context['sub_total_price'] = sub_total_price
        context['total_price'] = total_price
        context['shipping'] = shipping
        context['cart_items'] = CartItem.objects.filter(cart=cart)
        
        return context
    
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckOutSessionView(LoginRequiredMixin,generic.View):
    def post(self, *args, **kwargs):
        host = self.request.get_host()
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price_data':{
                        'currency':'usd',
                        'unit_amount':1000,
                        'product_data':{
                            'name':'book',
                        },
                        },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://{}{}".format(host,reverse('product:payment-success')),
            cancel_url="http://{}{}".format(host,reverse('product:payment-cancel')),
        )
        return redirect(checkout_session.url, code=303)
    
class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'product/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment-success"] = 'success'
        return context
    
class CheckoutCancelView(LoginRequiredMixin,TemplateView):
    template_name = 'product/payment_cancel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment-cancel"] = 'cancel'
        return context
    


class ProductSearchView(ListView):
    model = Product
    template_name = 'product/product_search_results.html'
    context_object_name = 'products_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Check for specific keywords
            if 'lap' in query.lower() or 'laptop' in query.lower():
                return Laptop.objects.all()
            if 'nin' in query.lower() or 'nintendo' in query.lower():
            
                return Nintendo.objects.filter(name__icontains=query)
            # General search across all products
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()