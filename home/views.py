from django.shortcuts import render,redirect,HttpResponse
from django.views.generic import (
    TemplateView,
)
from product.models import *

class HomeView(TemplateView):
    template_name = 'home/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the main category 'Shoe'
        shoe_category = MainCategoryModel.objects.get(main_category_name="Shoe")
        
        # Get the subcategories for 'Shoe'
        men_subcategory = SubCategoryModel.objects.get(main_category=shoe_category, sub_category_name="men")
        women_subcategory = SubCategoryModel.objects.get(main_category=shoe_category, sub_category_name="women")
        boys_subcategory = SubCategoryModel.objects.get(main_category=shoe_category, sub_category_name="boy")
        girls_subcategory = SubCategoryModel.objects.get(main_category=shoe_category, sub_category_name="girl")
        
        # Fetch and debug men shoes
        men_shoes = Shoe.objects.filter(sub_category=men_subcategory).order_by('?')[:4]
        print('Men Shoes:')
        for shoe in men_shoes:
            print('-----------', shoe.name, '--------------')
        
        # Fetch and debug women shoes
        women_shoes = Shoe.objects.filter(sub_category=women_subcategory).order_by('?')[:4]
        print('Women Shoes:')
        for shoe in women_shoes:
            print('-----------', shoe.name, '--------------')
        
        # Fetch and debug boys shoes
        boys_shoes = Shoe.objects.filter(sub_category=boys_subcategory).order_by('?')[:1]
        print('Boys Shoes:')
        for shoe in boys_shoes:
            print('-----------', shoe.name, '--------------')
        
        # Fetch and debug girls shoes
        girls_shoes = Shoe.objects.filter(sub_category=girls_subcategory).order_by('?')[:4]
        print('Girls Shoes:')
        for shoe in girls_shoes:
            print('-----------', shoe.name, '--------------')
        
        # Fetch and debug top selling boys shoes
        top_selling_boys_shoes = Shoe.objects.filter(sub_category=boys_subcategory).order_by('?')[:6]
        print('top_selling_boys_shoes:')
        for shoe in top_selling_boys_shoes:
            print('-----------', shoe.name, '--------------')
        
        # Fetch and debug top selling ggirls shoes
        top_selling_girls_shoes = Shoe.objects.filter(sub_category=girls_subcategory).order_by('?')[:6]
        print('top_selling_girls_shoes:')
        for shoe in top_selling_girls_shoes:
            print('-----------', shoe.name, '--------------')
        
        # Add to context
        context['men_shoes'] = men_shoes
        context['women_shoes'] = women_shoes
        context['boys_shoes'] = boys_shoes
        context['girls_shoes'] = girls_shoes
        
        context['top_selling_boys_shoes'] = top_selling_boys_shoes
        context['top_selling_girls_shoes'] = top_selling_girls_shoes
        
        return context