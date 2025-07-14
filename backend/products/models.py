from django.db import models
from .utils.cities import TURKISH_CITIES
from .utils.city_data import CITY_CHOICES, PROVINCE_MAP
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    SALE = 'sale'
    EXCHANGE = 'exchange'
    TYPE_CHOICES = [
        (SALE, 'Sale'),
        (EXCHANGE, 'Exchange'),
    ]

    listing_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=SALE,
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    exchange_for = models.ManyToManyField(Category, related_name='exchange_products', blank=True)
    exchange_details = models.TextField(blank=True, null=True)


    # Budget Range
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Barter Preferences
    will_give_extra_cash = models.BooleanField(default=False)
    will_receive_extra_cash = models.BooleanField(default=False)
    cannot_give_extra_cash = models.BooleanField(default=False)
    accept_half_cash = models.BooleanField(default=False)
    accept_half_barter = models.BooleanField(default=False)
    accept_full_barter = models.BooleanField(default=False)
    accept_full_cash = models.BooleanField(default=False)

    EXCHANGE_PREFERENCES = [
        ('will_give_extra_cash', "Üste Para Verilir"),
        ('will_receive_extra_cash', "Üste Para Alınır"),
        ('cannot_give_extra_cash', "Üste Para Veremem"),
        ('accept_half_cash', "%50 Nakit Talep Edilebilir"),
        ('accept_half_barter', "%50 Takas Talep Edilir"),
        ('accept_full_barter', "Tamamı Takas Olur"),
        ('accept_full_cash', "Tamamı Nakit Olur"),
    ]

    def has_exchange_preferences(self):
        return any([
            self.will_give_extra_cash,
            self.will_receive_extra_cash,
            self.cannot_give_extra_cash,
            self.accept_half_cash,
            self.accept_half_barter,
            self.accept_full_barter,
            self.accept_full_cash,
            self.min_budget is not None,
            self.max_budget is not None,
        ])

    # ✅ 2. Method to return readable preference labels
    def get_exchange_preference_labels(self):
        labels = []
        if self.will_give_extra_cash:
            labels.append("Will give extra cash")
        if self.will_receive_extra_cash:
            labels.append("Will receive extra cash")
        if self.cannot_give_extra_cash:
            labels.append("Cannot give extra cash")
        if self.accept_half_cash:
            labels.append("50% cash can be requested")
        if self.accept_half_barter:
            labels.append("50% barter can be requested")
        if self.accept_full_barter:
            labels.append("Full barter accepted")
        if self.accept_full_cash:
            labels.append("Full cash accepted")
        return labels

    # ✅ 3. Clean method to validate logic
    def clean(self):
        # Only validate if listing is 'exchange'
        if self.listing_type == 'exchange':
            if self.will_give_extra_cash and self.cannot_give_extra_cash:
                raise ValidationError("A product cannot both give and not give extra cash.")

        # Optional: Check budget consistency
        if self.min_budget and self.max_budget:
            if self.min_budget > self.max_budget:
                raise ValidationError("Minimum budget cannot be greater than maximum budget.")

    # Contact and address fields
    city = models.CharField(max_length=100, choices=CITY_CHOICES)  # E.g., Istanbul
    province = models.CharField(max_length=100)    
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class ExchangeNote(models.Model):
    product = models.ForeignKey('Product', related_name='exchange_notes', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} – {self.category.name}"


class ExchangeNoteItem(models.Model):
    note = models.ForeignKey(ExchangeNote, related_name='items', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')

    def __str__(self):
        return f"{self.product.name} - Image"

class ProductVideo(models.Model):
    product = models.ForeignKey(Product, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='product_videos/')
    thumbnail = models.ImageField(upload_to='product_videos/thumbnails/', blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - Video"
    

class ProductDetailRow(models.Model):
    product = models.ForeignKey(Product, related_name='detail_rows', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label}: {self.value}"
