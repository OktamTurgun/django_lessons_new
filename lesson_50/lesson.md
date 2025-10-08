# Lesson 50: ModelTranslation modulidan foydalanib modelni tarjima qilish

## Kirish

Oldingi darsda biz Django'ning `i18n` (internationalization) tizimi bilan tanishdik va statik matnlarni tarjima qilishni o'rgandik. Lekin veb-saytlarda faqat statik matnlar emas, balki **database'dagi ma'lumotlar** ham ko'p tillarda bo'lishi kerak. Masalan, yangiliklar, maqolalar, mahsulot nomlari va boshqa dinamik kontent.

Ushbu darsda biz **django-modeltranslation** kutubxonasi yordamida Django modellarimizni ko'p tilga tarjima qilishni o'rganamiz.

## Maqsad

- `django-modeltranslation` kutubxonasini o'rnatish va sozlash
- Model maydonlarini tarjima qilish uchun tayyorlash
- Tarjima fayllarini yaratish va to'ldirish
- Admin panelda tarjima maydonlarini ko'rsatish
- Template'larda tarjima qilingan ma'lumotlarni chiqarish

---

## 1. django-modeltranslation nima?

`django-modeltranslation` - bu Django modellari maydonlarini avtomatik ravishda ko'p tilga tarjima qilish imkonini beruvchi kuchli kutubxonadir.

### Asosiy xususiyatlari:

- Har bir maydon uchun tilga mos qo'shimcha maydonlar yaratadi
- Admin panelda tarjima maydonlarini avtomatik ko'rsatadi
- Joriy til bo'yicha avtomatik tarjimani qaytaradi
- Mavjud loyihaga oson integratsiya qilinadi

---

## 2. django-modeltranslation o'rnatish

### Qadam 1: Kutubxonani o'rnatish

Terminal orqali quyidagi buyruqni bajaring:

```bash
pip install django-modeltranslation
```

### Qadam 2: INSTALLED_APPS ga qo'shish

`settings.py` faylingizni oching va `INSTALLED_APPS` ro'yxatiga `modeltranslation` qo'shing.

**Muhim:** `modeltranslation` django.contrib.admin dan **oldin** turishi kerak!

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Modeltranslation - admindan oldin!
    'modeltranslation',
    
    # Sizning appalaringiz
    'news_app',
    'accounts_app',
]
```

**Eslatma:** Agar siz `modeltranslation`ni `admin`dan keyin qo'ysangiz, admin panelda tarjima maydonlari to'g'ri ko'rinmaydi!

---

## 3. Tillarni sozlash

`settings.py` faylida tillarni belgilang:

```python
# Asosiy til
LANGUAGE_CODE = 'uz'

# Qo'llab-quvvatlanadigan tillar
LANGUAGES = (
    ('uz', 'O\'zbekcha'),
    ('ru', 'Русский'),
    ('en', 'English'),
)

# Modeltranslation uchun standart til
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'

# Til kodlarini qisqartirish (ixtiyoriy)
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en')
```

---

## 4. Translation.py faylini yaratish

Har bir app uchun `translation.py` fayl yaratamiz. Bu faylda qaysi model maydonlarini tarjima qilish kerakligini belgilaymiz.

### Misol: news_app uchun translation.py

`news_app/translation.py` faylini yarating:

```python
from modeltranslation.translator import register, TranslationOptions
from .models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')  # Tarjima qilinadigan maydonlar


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # Kategoriya nomini tarjima qilamiz
```

**Tushuntirish:**

- `@register(News)` - News modelini tarjima uchun ro'yxatdan o'tkazamiz
- `fields = ('title', 'body')` - faqat title va body maydonlari tarjima qilinadi
- Siz istalgan maydonlarni qo'shishingiz mumkin, masalan: `fields = ('title', 'body', 'description')`

---

## 5. Migratsiya yaratish va qo'llash

Endi database'ga yangi tarjima maydonlarini qo'shish uchun migratsiya qilamiz:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Nima bo'ldi?**

`modeltranslation` har bir tarjima maydoniga yangi ustunlar qo'shadi:

- `title` → `title_uz`, `title_ru`, `title_en`
- `body` → `body_uz`, `body_ru`, `body_en`
- `name` → `name_uz`, `name_ru`, `name_en`

---

## 6. Admin panelni yangilash

### Oddiy variant (avtomatik)

`modeltranslation` admin panelda tarjima maydonlarini avtomatik ko'rsatadi. Siz hech narsa qilishingiz shart emas!

Admin panelga kiring va News modelini oching. Har bir maydon uchun 3 ta tab paydo bo'ladi (Uzbek, Russian, English).

### Qo'shimcha sozlash (ixtiyoriy)

Agar admin panelda qo'shimcha sozlash qilmoqchi bo'lsangiz:

```python
# news_app/admin.py
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import News, Category


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'publish_time', 'status')
    list_filter = ('status', 'category', 'publish_time')
    search_fields = ('title', 'body')
    
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)
```

---

## 7. Template'da tarjima qilingan ma'lumotlarni chiqarish

Template'da tarjima qilingan maydonlarni chiqarish juda oddiy - siz faqat maydon nomini yozasiz, `modeltranslation` avtomatik ravishda joriy tilga mos ma'lumotni qaytaradi.

### Misol: news_list.html

```html
{% load i18n %}

<div class="news-list">
    {% for news in news_list %}
    <div class="news-item">
        <h2>{{ news.title }}</h2>  <!-- Avtomatik joriy tildagi title -->
        <p>{{ news.body|truncatewords:30 }}</p>
        <a href="{% url 'news_detail' news.slug %}">{% trans "Batafsil" %}</a>
    </div>
    {% endfor %}
</div>
```

**Nima bo'ldi?**

- Agar joriy til `uz` bo'lsa → `news.title` `title_uz`ni qaytaradi
- Agar joriy til `ru` bo'lsa → `news.title` `title_ru`ni qaytaradi
- Agar joriy til `en` bo'lsa → `news.title` `title_en`ni qaytaradi

### Misol: news_detail.html

```html
{% load i18n %}

<article class="news-detail">
    <h1>{{ news.title }}</h1>
    
    <div class="news-meta">
        <span>{% trans "Kategoriya" %}: {{ news.category.name }}</span>
        <span>{% trans "Sana" %}: {{ news.publish_time|date:"d.m.Y" }}</span>
    </div>
    
    <div class="news-body">
        {{ news.body|safe }}
    </div>
</article>
```

---

## 8. Ma'lum bir tilda ma'lumot olish

Ba'zan siz joriy tildan qat'i nazar, ma'lum bir tildagi ma'lumotni olishingiz kerak bo'lishi mumkin:

```python
# Views.py da
from django.utils.translation import activate

def some_view(request):
    news = News.objects.get(id=1)
    
    # O'zbek tilidagi sarlavha
    uz_title = news.title_uz
    
    # Rus tilidagi sarlavha
    ru_title = news.title_ru
    
    # Ingliz tilidagi sarlavha
    en_title = news.title_en
    
    # Yoki tilni vaqtincha o'zgartirish
    activate('ru')
    russian_title = news.title  # Rus tilidagi sarlavha
    activate('uz')
    uzbek_title = news.title    # O'zbek tilidagi sarlavha
```

---

## 9. Mavjud ma'lumotlarni tarjima qilish

Agar sizda allaqachon ma'lumotlar mavjud bo'lsa, ularni yangi tarjima maydonlariga ko'chirish kerak.

### Usul 1: Admin panel orqali

1. Admin panelga kiring
2. Har bir yangilikni oching
3. Har bir til uchun ma'lumotlarni kiriting
4. Saqlang

### Usul 2: Django shell orqali

```bash
python manage.py shell
```

```python
from news_app.models import News

# Barcha yangiliklar uchun
for news in News.objects.all():
    # Agar title bosh bo'lsa, title_uz ga nusxa ko'chirish
    if not news.title_uz:
        news.title_uz = news.title
    if not news.body_uz:
        news.body_uz = news.body
    news.save()
```

### Usul 3: Management command yaratish

`news_app/management/commands/migrate_translations.py`:

```python
from django.core.management.base import BaseCommand
from news_app.models import News, Category


class Command(BaseCommand):
    help = 'Migrate existing data to translation fields'

    def handle(self, *args, **kwargs):
        # News modelini yangilash
        for news in News.objects.all():
            if not news.title_uz:
                news.title_uz = news.title
            if not news.body_uz:
                news.body_uz = news.body
            news.save()
        
        # Category modelini yangilash
        for category in Category.objects.all():
            if not category.name_uz:
                category.name_uz = category.name
            category.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully migrated translations'))
```

Ishga tushirish:

```bash
python manage.py migrate_translations
```

---

## 10. Fallback (zaxira) sozlamalari

Agar biror tilda tarjima bo'lmasa, modeltranslation standart tilga qaytadi.

`settings.py` da:

```python
# Agar tarjima topilmasa, standart tilga qaytish
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz', 'en')

# Yoki har bir til uchun alohida fallback
MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('uz', 'en'),
    'ru': ('uz',),
    'en': ('uz',),
}
```

---

## 11. Qidiruv funksiyasida tarjima

Agar sizda qidiruv funksiyasi bo'lsa, barcha tillarda qidirish uchun:

```python
# views.py
from django.db.models import Q

def search_news(request):
    query = request.GET.get('q')
    
    if query:
        news_list = News.objects.filter(
            Q(title_uz__icontains=query) |
            Q(title_ru__icontains=query) |
            Q(title_en__icontains=query) |
            Q(body_uz__icontains=query) |
            Q(body_ru__icontains=query) |
            Q(body_en__icontains=query)
        )
    else:
        news_list = News.objects.all()
    
    return render(request, 'news/search_results.html', {'news_list': news_list})
```

---

## 12. Slug maydonini tarjima qilish

Agar slug maydonini ham tarjima qilmoqchi bo'lsangiz:

```python
# translation.py
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body', 'slug')
```

Lekin odatda slug bir xil qoladi, chunki URL bir xil bo'lishi kerak.

---

## 13. Prepopulated fields admin panelda

Admin panelda slug maydonini title asosida avtomatik to'ldirish:

```python
# admin.py
@admin.register(News)
class NewsAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('title',)}
```

Agar slug ham tarjima qilinsa:

```python
@admin.register(News)
class NewsAdmin(TranslationAdmin):
    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug_uz': ('title_uz',),
            'slug_ru': ('title_ru',),
            'slug_en': ('title_en',),
        }
```

---

## 14. REST API bilan ishlash

Agar sizda Django REST Framework bo'lsa:

```python
# serializers.py
from rest_framework import serializers
from modeltranslation.utils import get_language
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'body', 'publish_time']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lang = self.context.get('language', get_language())
        
        # Ma'lum bir tilda ma'lumot qaytarish
        representation['title'] = getattr(instance, f'title_{lang}')
        representation['body'] = getattr(instance, f'body_{lang}')
        
        return representation
```

---

## Xulosa

Ushbu darsda biz `django-modeltranslation` kutubxonasi yordamida:

1. ✅ Modellarni tarjima qilishni o'rgandik
2. ✅ Admin panelda tarjima maydonlarini sozladik
3. ✅ Template'larda tarjima qilingan ma'lumotlarni chiqarishni ko'rdik
4. ✅ Mavjud ma'lumotlarni tarjimaga ko'chirishni o'rgandik
5. ✅ Fallback va qidiruv funksiyalarini sozladik

---

## Keyingi dars

Keyingi darsda biz **template'dagi statik matnlarni tarjima qilishni** batafsil ko'rib chiqamiz. Bu yerda biz `{% trans %}` va `{% blocktrans %}` teglaridan foydalanishni o'rganamiz.

---

## Best Practices va Maslahatlar

### 1. Migration tartibini to'g'ri bajaring

```bash
# 1. Modeltranslation o'rnatish
pip install django-modeltranslation

# 2. Settings.py ni yangilash
# INSTALLED_APPS ga modeltranslation qo'shish

# 3. translation.py faylini yaratish

# 4. Migratsiya
python manage.py makemigrations
python manage.py migrate
```

### 2. Tarjima maydonlarini to'ldirish

- Har doim **asosiy til**da ma'lumot kiriting
- Keyin boshqa tillarga tarjima qiling
- Bo'sh tarjimalar uchun fallback ishlatiladi

### 3. Performance (samaradorlik)

Agar ko'p til bo'lsa va ko'p ma'lumot bo'lsa, `select_related` va `prefetch_related` dan foydalaning:

```python
news_list = News.objects.select_related('category').all()
```

### 4. Admin panel sozlamalari

Admin panelda tillarni tab shaklida ko'rsatish uchun `TranslationAdmin` dan foydalaning.

### 5. Testing

Tarjimalarni test qilish uchun:

```python
from django.test import TestCase
from django.utils.translation import activate
from .models import News


class NewsTranslationTest(TestCase):
    def test_news_translation(self):
        news = News.objects.create(
            title_uz="O'zbek sarlavha",
            title_ru="Русский заголовок",
            title_en="English title"
        )
        
        activate('uz')
        self.assertEqual(news.title, "O'zbek sarlavha")
        
        activate('ru')
        self.assertEqual(news.title, "Русский заголовок")
        
        activate('en')
        self.assertEqual(news.title, "English title")
```

### 6. Git'ga o'zgarishlarni saqlash

```bash
git add .
git commit -m "Add django-modeltranslation for News and Category models"
git push origin main
```

---

## Muhim eslatmalar

⚠️ **Diqqat:**

1. `modeltranslation` **admin'dan oldin** `INSTALLED_APPS` da turishi kerak
2. `translation.py` fayli **har bir app** uchun alohida yaratiladi
3. Migratsiyadan keyin **mavjud ma'lumotlarni** yangi maydonlarga ko'chiring
4. Slug maydonini tarjima qilish **ixtiyoriy** (odatda bir xil qoladi)
5. Fallback sozlamalarini **to'g'ri** belgilang

---

## Qo'shimcha resurslar

- [django-modeltranslation dokumentatsiyasi](https://django-modeltranslation.readthedocs.io/)
- [Django i18n dokumentatsiyasi](https://docs.djangoproject.com/en/stable/topics/i18n/)
```