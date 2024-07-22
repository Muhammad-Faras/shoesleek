from django.urls import path
from . views import * 
app_name = 'product'
urlpatterns = [
    path('category/<str:category_name>', ProductCategoryView.as_view(),name='product_category'),
    path('list/<str:subcategory_name>/', ProductListView.as_view(),name='product_list'),
    path('detail/<str:product_type>/<str:product_name>/<int:pk>/', ProductDetailView.as_view(),name='product_detail'),
    path('cart/', ProductCartView.as_view(),name='product_cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('billing-info/', CheckoutView.as_view(),name='proceed-to-billing'),
    path('checkout/', CreateCheckOutSessionView.as_view(),name='create-checkout-session'),
    path('payment-success/', CheckoutSuccessView.as_view(),name='payment-success'),
    path('payment-cancel/', CheckoutCancelView.as_view(),name='payment-cancel'),
    path('search/', ProductSearchView.as_view(), name='search'),
]