# coding=utf-8

from django.contrib import admin
from models import Product,PurchaseLog
from django import forms

class ProductForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea,label='描述')
    class Meta:
        model = Product


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price', 'desc','is_alive','is_current',)
    search_fields = ('name','desc')
    list_per_page = 50
    list_filter = ('is_alive','is_current')
    ordering = ('id',)

admin.site.register(Product,ProductAdmin)

class PurchaseLogAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('ps', 'count', 'buyer','has_paid','create_time',)
    search_fields = ('ps__product',)
    list_per_page = 50
    list_filter = ('has_paid',)
    ordering = ('id',)

admin.site.register(PurchaseLog,PurchaseLogAdmin)