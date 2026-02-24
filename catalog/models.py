from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Role(models.Model):
    GUEST = 'guest'
    CLIENT = 'client'
    MANAGER = 'manager'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CLIENT, 'Авторизованный клиент'),
        (MANAGER, 'Менеджер'),
        (ADMIN, 'Администратор'),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class User(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name='ФИО', blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)

    def is_admin(self):
        return self.role and self.role.name == Role.ADMIN

    def is_manager(self):
        return self.role and self.role.name == Role.MANAGER

    def can_filter(self):
        return self.role and self.role.name in [Role.MANAGER, Role.ADMIN]

    def can_edit_products(self):
        return self.role and self.role.name == Role.ADMIN

    def can_view_orders(self):
        return self.role and self.role.name in [Role.MANAGER, Role.ADMIN]

    def can_edit_orders(self):
        return self.role and self.role.name == Role.ADMIN

    def __str__(self):
        return self.full_name or self.username


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Категория')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Производитель')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Поставщик')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    article = models.CharField(max_length=50, unique=True, verbose_name='Артикул')
    name = models.CharField(max_length=255, verbose_name='Наименование')
    unit = models.CharField(max_length=20, default='пара', verbose_name='Ед. изм.')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Цена'
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Скидка %'
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Остаток'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Фото')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.article} — {self.name}'

    def get_final_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def has_discount(self):
        return self.discount > 0

    def get_row_class(self):
        if self.stock == 0:
            return 'table-info'
        if self.discount > 15:
            return 'row-sale'
        return ''


class DeliveryPoint(models.Model):
    address = models.CharField(max_length=500, verbose_name='Адрес пункта выдачи')

    def __str__(self):
        return self.address


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новый'),
        (STATUS_COMPLETED, 'Завершён'),
        (STATUS_CANCELLED, 'Отменён'),
    ]

    number = models.IntegerField(unique=True, verbose_name='Номер заказа')
    article = models.CharField(max_length=50, verbose_name='Артикул')
    order_date = models.DateField(verbose_name='Дата заказа')
    delivery_date = models.DateField(null=True, blank=True, verbose_name='Дата доставки')
    client_name = models.CharField(max_length=255, verbose_name='ФИО клиента')
    pickup_code = models.CharField(max_length=20, verbose_name='Код получения')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name='Статус')
    delivery_point = models.ForeignKey(DeliveryPoint, on_delete=models.PROTECT, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f'Заказ №{self.number} ({self.client_name})'
