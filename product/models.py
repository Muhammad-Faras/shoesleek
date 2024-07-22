from django.db import models
from django.contrib.auth.models import User
class MainCategoryModel(models.Model):
    main_category_name = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-created_date'] 

    def __str__(self):
        return self.main_category_name
    
    
class SubCategoryModel(models.Model):
    main_category = models.ForeignKey(MainCategoryModel,on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='subcategory_images/', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-created_date'] 

    def __str__(self):
        return f'{self.sub_category_name} -> {self.main_category.main_category_name}'
    
class Color(models.Model):
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return self.color_name
    

class Product(models.Model):
    sub_category = models.ForeignKey(SubCategoryModel, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    colors = models.ManyToManyField(Color, blank=True)
    def __str__(self):
        return self.name

# Creating the Shoe model inheriting from Product
class Shoe(Product):
    fabric_type = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    sole_material = models.CharField(max_length=255)
    outer_material = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.origin}"
    





    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"