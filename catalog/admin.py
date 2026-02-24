from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Role, User, Category, Manufacturer, Supplier, Product, DeliveryPoint, Order


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'full_name', 'role', 'email', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('full_name', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('full_name', 'role')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['article', 'name', 'price', 'discount', 'stock', 'category', 'supplier']
    list_filter = ['category', 'supplier', 'manufacturer']
    search_fields = ['article', 'name']


@admin.register(DeliveryPoint)
class DeliveryPointAdmin(admin.ModelAdmin):
    list_display = ['address']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'client_name', 'article', 'order_date', 'status']
    list_filter = ['status']
    search_fields = ['number', 'client_name']
