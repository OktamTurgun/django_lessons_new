# Django 13-dars: Loyiha modelini tuzish

## Maqsad
Ushbu darsda siz Django da modellar yaratish, ularning o'zaro bog'lanishlarini tuzish va ma'lumotlar bazasi bilan samarali ishlashni o'rganasiz.

## Nazariy qism

### Model nima?
Model - bu ma'lumotlar bazasidagi jadvalning Python orqali ifodalanishi. Django da har bir model `django.db.models.Model` klassidan meros oladi.

### Asosiy Model turlari

#### 1. Oddiy Model
```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
```

**Tushuntirish:**
- `CharField` - matn maydonlari uchun
- `TextField` - uzun matnlar uchun
- `DateTimeField` - sana va vaqt uchun
- `auto_now_add=True` - yaratilgan vaqtni avtomatik saqlaydi
- `__str__` - obyektning matn ko'rinishini belgilaydi
- `Meta` klassi - model haqida qo'shimcha ma'lumotlar

#### 2. ForeignKey bog'lanishi
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products'
    )
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
```

**Tushuntirish:**
- `ForeignKey` - boshqa modelga havola
- `on_delete=models.CASCADE` - asosiy obyekt o'chirilganda bog'langan obyektlar ham o'chadi
- `related_name` - teskari bog'lanish nomi
- `DecimalField` - pul miqdorlari uchun
- `ordering` - obyektlarni tartiblash

#### 3. Many-to-Many bog'lanishi
```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
```

**Tushuntirish:**
- `ManyToManyField` - ko'pdan-ko'pga bog'lanish
- `auto_now=True` - har safar yangilanganda vaqtni saqlaydi
- `'auth.User'` - Django ning built-in User modeliga havola

## To'liq loyiha modeli misolini yaratish

### 1. E-commerce loyiha modeli

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def get_price(self):
        """Chegirma narxi bo'lsa uni qaytaradi, aks holda asosiy narxni"""
        if self.discount_price:
            return self.discount_price
        return self.price
    
    @property
    def is_in_stock(self):
        """Mahsulot omborda bormi?"""
        return self.stock > 0
    
    class Meta:
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.product.name} - rasm"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('confirmed', 'Tasdiqlandi'),
        ('shipped', 'Yuborildi'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
    ]
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Buyurtma #{self.id} - {self.customer.user.username}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.quantity * self.price

class Review(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.rating} yulduz"
    
    class Meta:
        unique_together = ['product', 'customer']  # Bir mahsulotga faqat bir marta sharh
        ordering = ['-created_at']
```

### 2. Migration yaratish va qo'llash

```bash
# Migration fayllarini yaratish
python manage.py makemigrations

# Migrationlarni qo'llash
python manage.py migrate
```

### 3. Admin panelda modellarni ro'yxatdan o'tkazish

```python
# admin.py
from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Customer, Order, OrderItem, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'stock', 'is_active']
    list_filter = ['category', 'brand', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer__user__username', 'customer__user__email']
    inlines = [OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'customer__user__username']

admin.site.register(Brand)
admin.site.register(Customer)
```

## ORM bilan ishlash misollari

### 1. Ma'lumotlar qo'shish
```python
# views.py yoki Django shell da
from .models import Category, Product, Brand

# Kategoriya yaratish
category = Category.objects.create(
    name="Elektronika",
    slug="elektronika",
    description="Elektronika mahsulotlari"
)

# Brand yaratish
brand = Brand.objects.create(name="Samsung")

# Mahsulot yaratish
product = Product.objects.create(
    name="Samsung Galaxy S21",
    slug="samsung-galaxy-s21",
    description="Zamonaviy smartphone",
    price=800.00,
    category=category,
    brand=brand,
    stock=50
)
```

### 2. Ma'lumotlarni o'qish
```python
# Barcha mahsulotlar
products = Product.objects.all()

# Faol mahsulotlar
active_products = Product.objects.filter(is_active=True)

# Kategoriya bo'yicha mahsulotlar
electronics = Product.objects.filter(category__name="Elektronika")

# Narx oralig'i bo'yicha
expensive_products = Product.objects.filter(price__gte=500)

# Kompleks so'rovlar
samsung_phones = Product.objects.filter(
    brand__name="Samsung",
    category__name="Elektronika",
    stock__gt=0
)
```

### 3. Related obyektlar bilan ishlash
```python
# Mahsulot va uning kategoriyasi
product = Product.objects.select_related('category', 'brand').get(id=1)
print(product.category.name)
print(product.brand.name)

# Kategoriya va uning mahsulotlari
category = Category.objects.prefetch_related('products').get(id=1)
for product in category.products.all():
    print(product.name)

# Buyurtma va uning elementlari
order = Order.objects.prefetch_related('items__product').get(id=1)
for item in order.items.all():
    print(f"{item.product.name} - {item.quantity} ta")
```

## Custom metodlar va property'lar

```python
class Product(models.Model):
    # ... maydonlar ...
    
    @property
    def average_rating(self):
        """Mahsulotning o'rtacha reytingi"""
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0
    
    @property
    def review_count(self):
        """Sharhlar soni"""
        return self.reviews.count()
    
    def is_on_sale(self):
        """Chegirmada ekanligini tekshirish"""
        return self.discount_price is not None
    
    def get_main_image(self):
        """Asosiy rasmni olish"""
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image.image.url
        return None
    
    class Meta:
        ordering = ['-created_at']
```

## Model Validation

```python
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class Product(models.Model):
    # ... boshqa maydonlar ...
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    
    def clean(self):
        """Custom validation"""
        if self.discount_price and self.discount_price >= self.price:
            raise ValidationError('Chegirma narxi asosiy narxdan kichik bo\'lishi kerak')
    
    def save(self, *args, **kwargs):
        """Custom save metodi"""
        self.clean()  # Validatsiyani chaqirish
        super().save(*args, **kwargs)
```

## Signals bilan ishlash

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer

@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    """User yaratilganda Customer profili ham yaratiladi"""
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer_profile(sender, instance, **kwargs):
    """User saqlanganida Customer profili ham saqlanadi"""
    if hasattr(instance, 'customer'):
        instance.customer.save()
```

## Database Indexlar va Optimizatsiya

```python
class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)  # Index qo'shish
    slug = models.SlugField(max_length=200, unique=True)
    # ... boshqa maydonlar ...
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_active']),  # Composite index
            models.Index(fields=['-created_at']),  # Teskari tartib index
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0), 
                name='price_non_negative'
            ),
        ]
```

## Best Practices

1. **Model nomlarini to'g'ri tanlang**: Singular shakl ishlatiling (Product, Category)
2. **`__str__` metodini doim yozing**: Admin panelda ko'rish uchun
3. **Related_name ishlatiling**: Teskari bog'lanishlar uchun
4. **Meta klassidan foydalaning**: Ordering, verbose_name uchun
5. **Validatsiya qo'shing**: Ma'lumotlar to'g'riligini ta'minlash uchun
6. **Index qo'ying**: Tez-tez qidiriluvchi maydonlarga
7. **Select_related/Prefetch_related ishlatiling**: N+1 muammosini oldini olish uchun
8. **Custom metodlar yozing**: Takroriy logikani modelga joylashtiring

## news_project uchun Model misoli

Agar siz avvalgi darslarimizda yaratgan news_project loyihasi ustida ishlayotgan bo'lsangiz, quyidagi modelni ham qo'shishingiz mumkin:

### 1. News app uchun to'liq model

```python
# news/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL nomi")
    description = models.TextField(blank=True, verbose_name="Tavsifi")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('news:category_detail', kwargs={'slug': self.slug})
    
    @property
    def active_news_count(self):
        return self.news.filter(is_published=True).count()
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nomi")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="URL nomi")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Teg"
        verbose_name_plural = "Teglar"
        ordering = ['name']

class NewsManager(models.Manager):
    def published(self):
        return self.filter(is_published=True, publish_date__lte=timezone.now())

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL nomi")
    content = models.TextField(verbose_name="Matn")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="Qisqa mazmuni")
    
    # Media
    featured_image = models.ImageField(
        upload_to='news/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Asosiy rasm"
    )
    
    # Relationships
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='news',
        verbose_name="Muallif"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='news',
        verbose_name="Kategoriya"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Teglar")
    
    # Status and dates
    is_published = models.BooleanField(default=False, verbose_name="Nashr etilganmi")
    publish_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Nashr sanasi"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_description = models.CharField(
        max_length=160, 
        blank=True,
        verbose_name="Meta tavsifi"
    )
    
    # Stats
    views_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    
    objects = models.Manager()  # Default manager
    published_objects = NewsManager()  # Custom manager
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.excerpt and self.content:
            # Agar excerpt bo'sh bo'lsa, content dan olish
            self.excerpt = self.content[:300] + "..." if len(self.content) > 300 else self.content
        
        super().save(*args, **kwargs)
        
        # Rasmni resize qilish
        if self.featured_image:
            img = Image.open(self.featured_image.path)
            if img.height > 800 or img.width > 1200:
                img.thumbnail((1200, 800))
                img.save(self.featured_image.path)
    
    @property
    def reading_time(self):
        """Taxminiy o'qish vaqti (daqiqada)"""
        words = len(self.content.split())
        return max(1, words // 200)  # 200 so'z/daqiqa
    
    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', 'publish_date']),
            models.Index(fields=['category', 'is_published']),
        ]

class Comment(models.Model):
    news = models.ForeignKey(
        News, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Yangilik"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Muallif"
    )
    content = models.TextField(verbose_name="Sharh")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Parent comment for replies
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='replies',
        verbose_name="Javob"
    )
    
    def __str__(self):
        return f"{self.author.username} - {self.news.title[:30]}"
    
    @property
    def is_reply(self):
        return self.parent is not None
    
    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['created_at']

class NewsView(models.Model):
    """Yangilik ko'rishlarini kuzatish"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ko'rish"
        verbose_name_plural = "Ko'rishlar"
        unique_together = ['news', 'user', 'ip_address']  # Bir user bir yangiliknifaqat bir marta ko'rishi hisoblanadi
```

### 2. Admin panel sozlash

```python
# news/admin.py
from django.contrib import admin
from .models import Category, Tag, News, Comment, NewsView

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active_news_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_at']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'views_count', 'publish_date']
    list_filter = ['is_published', 'category', 'author', 'publish_date']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'reading_time']
    inlines = [CommentInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Kontent', {
            'fields': ('content', 'excerpt', 'featured_image', 'tags')
        }),
        ('Nashr sozlamalari', {
            'fields': ('is_published', 'publish_date')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
        ('Statistika', {
            'fields': ('views_count', 'reading_time', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratilayotgan bo'lsa
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'news', 'is_approved', 'is_reply', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author__username', 'news__title', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Tanlangan sharhlarni tasdiqlash"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Tanlangan sharhlar tasdiqini bekor qilish"

@admin.register(NewsView)
class NewsViewAdmin(admin.ModelAdmin):
    list_display = ['news', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['news__title', 'user__username']
```

### 3. Signals qo'shish

```python
# news/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News, NewsView

@receiver(post_save, sender=NewsView)
def update_news_view_count(sender, instance, created, **kwargs):
    """Yangi view qo'shilganda news'ning view_count'ini yangilash"""
    if created:
        news = instance.news
        news.views_count = news.news_views.count()
        news.save(update_fields=['views_count'])
```

### 4. news_project loyihasiga birlashtirish

```python
# news_project/settings.py
INSTALLED_APPS = [
    # ... boshqa app'lar
    'news',
]
```

Bu model news_project loyihasi uchun to'liq yangiliklar tizimini ta'minlaydi va barcha zamonaviy imkoniyatlarni o'z ichiga oladi.

## Xulosa

Modellar Django loyihasining asosini tashkil etadi. To'g'ri tuzilgan modellar loyihangizni samarali va kengaytiriladigan qiladi. Modellar o'rtasidagi bog'lanishlarni to'g'ri tashkil etish va ORM imkoniyatlaridan to'liq foydalanish muhimdir.