from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Order, User, DeliveryPoint


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
    )


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'article', 'name', 'unit', 'price', 'discount',
            'stock', 'description', 'image',
            'category', 'manufacturer', 'supplier',
        ]
        widgets = {
            'article':      forms.TextInput(attrs={'class': 'form-control'}),
            'name':         forms.TextInput(attrs={'class': 'form-control'}),
            'unit':         forms.TextInput(attrs={'class': 'form-control'}),
            'price':        forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount':     forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock':        forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image':        forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category':     forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
            'supplier':     forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'article':      'Артикул',
            'name':         'Наименование',
            'unit':         'Ед. изм.',
            'price':        'Цена, ₽',
            'discount':     'Скидка, %',
            'stock':        'Остаток',
            'description':  'Описание',
            'image':        'Изображение',
            'category':     'Категория',
            'manufacturer': 'Производитель',
            'supplier':     'Поставщик',
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            'number', 'article', 'order_date', 'delivery_date',
            'client_name', 'pickup_code', 'status', 'delivery_point', 'client',
        ]
        widgets = {
            'number':         forms.NumberInput(attrs={'class': 'form-control'}),
            'article':        forms.TextInput(attrs={'class': 'form-control'}),
            'order_date':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'delivery_date':  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'client_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_code':    forms.TextInput(attrs={'class': 'form-control'}),
            'status':         forms.Select(attrs={'class': 'form-select'}),
            'delivery_point': forms.Select(attrs={'class': 'form-select'}),
            'client':         forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'number':         'Номер заказа',
            'article':        'Артикул',
            'order_date':     'Дата заказа',
            'delivery_date':  'Дата доставки',
            'client_name':    'ФИО клиента',
            'pickup_code':    'Код получения',
            'status':         'Статус',
            'delivery_point': 'Пункт выдачи',
            'client':         'Клиент',
        }
