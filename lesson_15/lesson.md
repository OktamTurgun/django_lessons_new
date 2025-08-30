# Django Lesson 14: Django QuerySet va Model Manager

## 1. Asosiy Tushunchalar

### QuerySet nima?
**QuerySet** - Django ORM da ma'lumotlar bazasidan ma'lumotlarni olish vositasi. SQL so'rovlarining Python tilida ifodalanishi.

**Asosiy xususiyatlari:**
- **Lazy evaluation** - faqat kerak bo'lganda bajariladi
- **Chainable** - metodlarni zanjirlab ishlatish mumkin
- **Reusable** - bir marta yaratib, qayta ishlatish mumkin

### Model Manager nima?
**Manager** - model va database o'rtasidagi interface. Har bir model avtomatik `objects` managerga ega.

## 2. Asosiy CRUD Operatsiyalari

### Create (Yaratish)
```python
# 1-usul: Obyekt yaratib save qilish
news = News(title='Yangilik', content='Matn')
news.save()

# 2-usul: create() metodi
news = News.objects.create(
    title='Yangilik',
    content='Matn',
    status='published'
)

# 3-usul: get_or_create()
news, created = News.objects.get_or_create(
    slug='yangilik-slug',
    defaults={'title': 'Yangilik', 'content': 'Matn'}
)

# 4-usul: bulk_create() - ko'p obyekt
news_list = [
    News(title='Yangilik 1', content='Matn 1'),
    News(title='Yangilik 2', content='Matn 2'),
]
News.objects.bulk_create(news_list)
```

### Read (O'qish)
```python
# Barcha obyektlar
all_news = News.objects.all()

# Filtrlash
published = News.objects.filter(status='published')
not_draft = News.objects.exclude(status='draft')

# Bitta obyekt
news = News.objects.get(id=1)
first = News.objects.first()
last = News.objects.last()

# Xavfsiz olish
from django.shortcuts import get_object_or_404
news = get_object_or_404(News, slug='test-slug')

# Mavjudlik tekshirish
exists = News.objects.filter(slug='test').exists()

# Sanalash
count = News.objects.count()

# Saralash
by_date = News.objects.order_by('-created_at')
by_title = News.objects.order_by('title')

# Cheklash
latest_5 = News.objects.all()[:5]
random_3 = News.objects.order_by('?')[:3]

# Faqat ma'lum fieldlar
titles = News.objects.values('title', 'slug')
title_list = News.objects.values_list('title', flat=True)
```

### Update (Yangilash)
```python
# Bitta obyekt
news = News.objects.get(id=1)
news.title = 'Yangilangan title sarlavxasi yoziladi'
news.save()

# Ko'p obyekt
News.objects.filter(status='draft').update(status='published')

# F expression bilan
from django.db.models import F
News.objects.filter(id=1).update(views=F('views') + 1)

# update_or_create
news, created = News.objects.update_or_create(
    slug='test-slug',
    defaults={'title': 'Yangilangan'}
)
```

### Delete (O'chirish)
```python
# Bitta obyekt
news = News.objects.get(id=1)
news.delete()

# Ko'p obyekt
News.objects.filter(status='archived').delete()

# Barcha obyektlar (EHTIYOTKORLIK!)
News.objects.all().delete()
```

## 3. Ilg'or Filtrlash

### Matn bilan ishlash
```python
# Case-insensitive qidiruv
News.objects.filter(title__icontains='django')

# Boshlanish/tugash
News.objects.filter(title__startswith='Python')
News.objects.filter(title__endswith='tutorial')

# Regex
News.objects.filter(title__regex=r'^Django.*[0-9]+$')

# Aniq mos kelish
News.objects.filter(title__exact='Django Tutorial')
News.objects.filter(title__iexact='django tutorial')
```

### Raqamlar bilan ishlash
```python
# Taqqoslash
News.objects.filter(views__gt=100)      # >
News.objects.filter(views__gte=100)     # >=
News.objects.filter(views__lt=1000)     # <
News.objects.filter(views__lte=1000)    # <=

# Oraliq
News.objects.filter(views__range=(100, 1000))

# Ro'yxat
News.objects.filter(views__in=[100, 200, 500])
```

### Sana va vaqt
```python
from datetime import date, datetime, timedelta
from django.utils import timezone

# Aniq sana
News.objects.filter(created_at__date=date(2024, 1, 15))

# Yil, oy, kun
News.objects.filter(created_at__year=2024)
News.objects.filter(created_at__month=1)
News.objects.filter(created_at__day=15)

# Vaqt
News.objects.filter(created_at__time__gt='10:00:00')
News.objects.filter(created_at__hour=10)

# So'nggi 7 kun
last_week = timezone.now() - timedelta(days=7)
News.objects.filter(created_at__gte=last_week)
```

### Q Objects - Murakkab shartlar
```python
from django.db.models import Q

# OR sharti
News.objects.filter(
    Q(title__icontains='Django') | Q(title__icontains='Python')
)

# NOT sharti
News.objects.filter(~Q(status='draft'))

# Murakkab kombinatsiya
News.objects.filter(
    (Q(status='published') & Q(is_featured=True)) |
    (Q(status='draft') & Q(author=request.user))
)
```

## 4. Relationships

### ForeignKey (Forward)
```python
# Bog'langan obyekt orqali filtrlash
News.objects.filter(category__name='Texnologiya')
News.objects.filter(author__username='admin')
News.objects.filter(author__email__endswith='@gmail.com')

# Ko'p daraja
News.objects.filter(category__parent__name='IT')
```

### Reverse ForeignKey
```python
# Teskari bog'lanish
Category.objects.filter(news__status='published')
Category.objects.filter(news__views__gt=1000)
```

### ManyToMany
```python
# ManyToMany bog'lanishlar
News.objects.filter(tags__name='python')
News.objects.filter(tags__name__in=['python', 'django'])
```

## 5. Aggregation va Annotation

### Aggregate - bitta qiymat
```python
from django.db.models import Count, Sum, Avg, Max, Min

stats = News.objects.aggregate(
    total=Count('id'),
    total_views=Sum('views'),
    avg_views=Avg('views'),
    max_views=Max('views')
)
# Natija: {'total': 150, 'total_views': 50000, ...}
```

### Annotate - har obyekt uchun
```python
# Har yangilik uchun comment soni
news_with_comments = News.objects.annotate(
    comment_count=Count('comments')
).filter(comment_count__gt=5)

# Kategoriyalar statistikasi
categories_with_stats = Category.objects.annotate(
    news_count=Count('news'),
    published_count=Count('news', filter=Q(news__status='published')),
    total_views=Sum('news__views')
)
```

## 6. Performance Optimizatsiya

### N+1 Problemasini Hal Qilish

#### select_related (ForeignKey/OneToOne)
```python
# Muammo - har yangilik uchun alohida query
news_list = News.objects.all()[:10]
for news in news_list:
    print(news.category.name)  # Extra query!

# Yechim
news_list = News.objects.select_related('category', 'author')[:10]
for news in news_list:
    print(news.category.name)  # Extra query yo'q!
```

#### prefetch_related (ManyToMany/Reverse FK)
```python
# ManyToMany uchun
news_list = News.objects.prefetch_related('tags')[:10]
for news in news_list:
    for tag in news.tags.all():  # Extra query yo'q!
        print(tag.name)
```

### Faqat kerakli fieldlar
```python
# Faqat ma'lum fieldlar
News.objects.only('title', 'created_at')

# Ba'zi fieldlarni keyinroq
News.objects.defer('content')
```

## 7. Custom Manager yaratish

```python
class NewsManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(status='published')
    
    def by_category(self, category_name):
        return self.published().filter(category__name=category_name)
    
    def recent(self, days=7):
        from django.utils import timezone
        from datetime import timedelta
        since = timezone.now() - timedelta(days=days)
        return self.published().filter(created_at__gte=since)
    
    def popular(self, limit=5):
        return self.published().order_by('-views')[:limit]

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
    ])
    views = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = NewsManager()  # Custom manager

# Ishlatish
News.objects.published()              # Nashr qilinganlar
News.objects.by_category('Tech')      # Kategoriya bo'yicha
News.objects.recent(30)               # So'nggi 30 kun
News.objects.popular(10)              # Top 10 mashhur
```

## 8. Custom QuerySet

```python
class NewsQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')
    
    def by_author(self, author):
        return self.filter(author=author)
    
    def search(self, query):
        return self.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

class NewsManager(models.Manager):
    def get_queryset(self):
        return NewsQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class News(models.Model):
    # ... fieldlar ...
    objects = NewsManager()

# Zanjirlab ishlatish
News.objects.published().by_author(user).search('Django')
```

## 9. QuerySet Qo'llanish Joylari

### Views da
```python
def news_list(request):
    news = News.objects.filter(status='published').select_related('category')
    
    # Filtrlash
    category_id = request.GET.get('category')
    if category_id:
        news = news.filter(category_id=category_id)
    
    return render(request, 'news/list.html', {'news_list': news})
```

### Templates da
```html
{% for news in news_list %}
    <h2>{{ news.title }}</h2>
    <p>{{ news.category.name }}</p>
{% empty %}
    <p>Yangiliklar yo'q</p>
{% endfor %}
```

### Template Tags da
```python
@register.simple_tag
def get_recent_news(count=5):
    return News.objects.filter(
        status='published'
    ).order_by('-created_at')[:count]
```

### Forms da
```python
class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            is_active=True
        ).order_by('name')
```

## 10. Database Functions

```python
from django.db.models import F, Value, Concat
from django.db.models.functions import Upper, Lower

# F expressions
News.objects.filter(views__gt=F('likes') * 2)

# Annotations
News.objects.annotate(
    full_title=Concat('title', Value(' - '), 'subtitle'),
    upper_title=Upper('title')
)
```

## 11. QuerySet Evaluation

QuerySet qachon bajariladi:
```python
queryset = News.objects.filter(status='published')  # Hali bajarilmagan

# Quyidagilar query ni bajaradi:
list(queryset)        # List ga aylantirish
len(queryset)         # Uzunlik
bool(queryset)        # Boolean tekshirish
for news in queryset: # Iteratsiya
queryset[0]           # Index bilan olish
```

## 12. Caching

```python
# QuerySet cache
queryset = News.objects.filter(status='published')
articles = list(queryset)  # Birinchi query
for article in queryset:   # Cache dan olinadi
    print(article.title)
```

## 13. Best Practices

1. **Lazy loading** - faqat kerak bo'lganda ma'lumot oling
2. **select_related/prefetch_related** - N+1 problemasini oldini oling
3. **Custom manager** - takrorlanuvchi logikani markazlashtiring
4. **Indexing** - ko'p ishlatiladigan fieldlarga index qo'shing
5. **only/defer** - faqat kerakli fieldlarni oling

## 14. Debug va Monitoring

```python
# SQL ko'rish
print(queryset.query)

# Query count tekshirish
from django.db import connection
print(len(connection.queries))

# Explain
queryset.explain()
```

## Xulosa

QuerySet va Manager Django ning eng kuchli vositalari. Ular orqali:
- Samarali database operatsiyalari
- Performance optimizatsiya
- Kodning qayta ishlatilishi
- Biznes logikaning markazlashtirilishi

mumkin bo'ladi.