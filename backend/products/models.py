from django.db import models

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

    # Contact and address fields
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_gallery/')

    def __str__(self):
        return f"{self.product.name} - Image"