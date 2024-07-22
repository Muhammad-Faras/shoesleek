from django.contrib import admin
from .models import *

class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('main_category_name', 'created_date') 

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name', 'created_date') 


admin.site.register(MainCategoryModel, MainCategoryAdmin)
admin.site.register(SubCategoryModel, SubCategoryAdmin)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Shoe)







admin.site.register(Cart)
admin.site.register(CartItem)