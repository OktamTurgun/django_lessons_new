# lesson 42 Ruxsatnomalar. Admin sahifasi ochish. Dekoratorli ruxsatnomalar

## Kirish

Django loyihalarimizda xavfsizlik va ruxsatnomalarni boshqarish juda muhim masaladir. Oldingi darslarimizda `LoginRequiredMixin` yordamida foydalanuvchilarni autentifikatsiya qilishni o'rgandik. Ushbu darsda biz quyidagilarni o'rganamiz:

- **UserPassesTestMixin** - maxsus shartlar asosida ruxsat berish
- **Admin sahifasini ochish** - barcha foydalanuvchilar uchun admin panel
- **Dekoratorli ruxsatnomalar** - funksiya-based view'larda ruxsatlarni boshqarish

---

## 1. UserPassesTestMixin nima?

`UserPassesTestMixin` - bu Django'ning class-based view'larda foydalaniladigan mixin bo'lib, u foydalanuvchining ma'lum bir testdan o'tishini talab qiladi.

### LoginRequiredMixin vs UserPassesTestMixin

**LoginRequiredMixin** - faqat foydalanuvchi tizimga kirganligini tekshiradi:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'body']
    template_name = 'news/update.html'
```

**UserPassesTestMixin** - maxsus shartlarni tekshiradi:

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView

class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author
```

---

## 2. UserPassesTestMixin'dan foydalanish

### 2.1. Asosiy sintaksis

`UserPassesTestMixin`dan foydalanish uchun `test_func()` metodini yozishimiz kerak:

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from .models import News

class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'category', 'image']
    template_name = 'news/update.html'
    
    def test_func(self):
        """
        Bu metod True yoki False qaytarishi kerak
        True - ruxsat beriladi
        False - 403 Forbidden xato
        """
        news = self.get_object()  # Hozirgi yangilikni olamiz
        return self.request.user == news.author  # Foydalanuvchi muallif ekanligini tekshiramiz
```

**Tushuntirish:**
- `test_func()` - ruxsatni tekshirish funksiyasi
- `self.get_object()` - hozirgi obyektni oladi (URL'dan ID yoki slug orqali)
- Agar foydalanuvchi maqola muallifi bo'lsa - `True` qaytaradi
- Aks holda - `False` qaytaradi va 403 xato chiqadi

### 2.2. DeleteView uchun misol

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from .models import News

class NewsDeleteView(UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
    
    def test_func(self):
        news = self.get_object()
        # Faqat muallif o'z yangiligini o'chirishi mumkin
        return self.request.user == news.author
```

### 2.3. Murakkab shartlar

Ba'zan bir nechta shartlarni tekshirish kerak bo'ladi:

```python
class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'category']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        user = self.request.user
        
        # Muallif yoki staff foydalanuvchi tahrirlashi mumkin
        return user == news.author or user.is_staff
```

**Boshqa misol:**

```python
class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'category']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        user = self.request.user
        
        # Bir necha shartlar
        if not user.is_authenticated:
            return False
        
        if user.is_superuser:
            return True
            
        if user == news.author and news.status == 'draft':
            return True
            
        return False
```

---

## 3. Admin sahifasini ochish

Odatiy holatda Django admin paneli faqat `is_staff=True` bo'lgan foydalanuvchilar uchun ochiq. Ammo ba'zan barcha foydalanuvchilar uchun admin panelini ochish kerak bo'ladi.

### 3.1. Barcha foydalanuvchilar uchun admin panelni ochish

**1-usul: settings.py orqali (tavsiya etilmaydi)**

Bu usul xavfsiz emas, chunki barcha foydalanuvchilar admin panelga kirishlari mumkin bo'ladi.

**2-usul: Custom AdminSite yaratish (to'g'ri usul)**

`news/admin.py` faylida:

```python
from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import News, Category

# Custom Admin Site yaratamiz
class CustomAdminSite(AdminSite):
    site_header = 'Yangiliklar Boshqaruvi'
    site_title = 'Admin Panel'
    index_title = 'Boshqaruv Paneli'
    
    def has_permission(self, request):
        """
        Barcha tizimga kirgan foydalanuvchilarga ruxsat beramiz
        """
        return request.user.is_active

# Custom admin site'ni yaratamiz
custom_admin_site = CustomAdminSite(name='custom_admin')

# Modellarni ro'yxatdan o'tkazamiz
@admin.register(News, site=custom_admin_site)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'publish_time', 'status']
    list_filter = ['status', 'category', 'publish_time']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    
    def save_model(self, request, obj, form, change):
        if not change:  # Yangi obyekt yaratilayotgan bo'lsa
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Oddiy foydalanuvchilar faqat o'z yangiliklarini ko'radi
        return qs.filter(author=request.user)

@admin.register(Category, site=custom_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
```

### 3.2. URL'ni sozlash

`config/urls.py` faylida:

```python
from django.contrib import admin
from django.urls import path, include
from news.admin import custom_admin_site  # Import qilamiz

urlpatterns = [
    path('admin/', admin.site.urls),  # Django'ning standart admin paneli
    path('my-admin/', custom_admin_site.urls),  # Bizning custom admin panelimiz
    path('', include('pages.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('accounts.urls')),
]
```

**Tushuntirish:**
- `admin/` - faqat superuser uchun
- `my-admin/` - barcha tizimga kirgan foydalanuvchilar uchun

### 3.3. Foydalanuvchiga faqat o'z ma'lumotlarini ko'rsatish

```python
@admin.register(News, site=custom_admin_site)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'publish_time']
    
    def get_queryset(self, request):
        """
        Har bir foydalanuvchi faqat o'z yangiliklarini ko'radi
        """
        qs = super().get_queryset(request)
        
        # Agar superuser bo'lsa - hamma narsani ko'radi
        if request.user.is_superuser:
            return qs
        
        # Oddiy foydalanuvchi faqat o'z yangiliklarini ko'radi
        return qs.filter(author=request.user)
    
    def has_delete_permission(self, request, obj=None):
        """
        Foydalanuvchi faqat o'z yangiligini o'chirishi mumkin
        """
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """
        Foydalanuvchi faqat o'z yangiligini o'zgartirishi mumkin
        """
        if obj is None:
            return True
        return obj.author == request.user or request.user.is_superuser
```

---

## 4. Dekoratorli ruxsatnomalar (Function-Based Views)

Class-based view'larda mixin'lardan foydalansak, function-based view'larda dekoratorlardan foydalanamiz.

### 4.1. @login_required dekoratori

Bu dekorator foydalanuvchi tizimga kirganligini tekshiradi:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from .forms import NewsForm

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    
    return render(request, 'news/create.html', {'form': form})
```

**Login URL'ni o'zgartirish:**

```python
@login_required(login_url='/accounts/login/')
def news_create(request):
    # kod
    pass
```

### 4.2. @user_passes_test dekoratori

Bu dekorator maxsus shartlarni tekshiradi:

```python
from django.contrib.auth.decorators import user_passes_test

def is_author(user):
    """
    Foydalanuvchi staff yoki superuser ekanligini tekshiradi
    """
    return user.is_staff or user.is_superuser

@user_passes_test(is_author)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    
    return render(request, 'news/create.html', {'form': form})
```

**Login URL bilan:**

```python
@user_passes_test(is_author, login_url='/accounts/login/')
def news_create(request):
    # kod
    pass
```

### 4.3. Murakkab tekshirishlar

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

@login_required
def news_update(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    # Foydalanuvchi muallif ekanligini tekshiramiz
    if request.user != news.author and not request.user.is_superuser:
        return HttpResponseForbidden("Sizda bu yangilikni tahrirlash huquqi yo'q!")
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'news/update.html', {'form': form, 'news': news})
```

### 4.4. @permission_required dekoratori

Django'ning o'rnatilgan ruxsatnomalaridan foydalanish:

```python
from django.contrib.auth.decorators import permission_required

@permission_required('news.add_news', raise_exception=True)
def news_create(request):
    # Faqat 'add_news' ruxsati bo'lgan foydalanuvchilar
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    
    return render(request, 'news/create.html', {'form': form})
```

**Bir nechta ruxsatlar:**

```python
@permission_required(['news.add_news', 'news.change_news'], raise_exception=True)
def news_manage(request):
    # kod
    pass
```

---

## 5. Custom ruxsatnomalar yaratish

### 5.1. Custom dekorator yaratish

`news/decorators.py` faylini yaratamiz:

```python
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from functools import wraps

def author_required(view_func):
    """
    Foydalanuvchi yangilik muallifi ekanligini tekshiradi
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        from .models import News
        
        # pk yoki slug orqali obyektni topamiz
        pk = kwargs.get('pk')
        slug = kwargs.get('slug')
        
        if pk:
            news = get_object_or_404(News, pk=pk)
        elif slug:
            news = get_object_or_404(News, slug=slug)
        else:
            return HttpResponseForbidden("Noto'g'ri so'rov!")
        
        # Tekshirish
        if request.user != news.author and not request.user.is_superuser:
            return HttpResponseForbidden("Sizda bu yangilikni tahrirlash huquqi yo'q!")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
```

**Foydalanish:**

```python
from django.contrib.auth.decorators import login_required
from .decorators import author_required

@login_required
@author_required
def news_update(request, pk):
    news = get_object_or_404(News, pk=pk)
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'news/update.html', {'form': form, 'news': news})
```

### 5.2. Custom mixin yaratish

Class-based view'lar uchun custom mixin:

`news/mixins.py` faylini yaratamiz:

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Foydalanuvchi obyekt muallifi ekanligini tekshiradi
    """
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        
        # Superuser har doim ruxsat oladi
        if user.is_superuser:
            return True
        
        # Muallif ekanligini tekshirish
        return obj.author == user
```

**Foydalanish:**

```python
from django.views.generic import UpdateView, DeleteView
from .mixins import AuthorRequiredMixin
from .models import News

class NewsUpdateView(AuthorRequiredMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'category', 'image']
    template_name = 'news/update.html'

class NewsDeleteView(AuthorRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
```

---

## 6. Template'da ruxsatlarni tekshirish

### 6.1. Foydalanuvchi tizimga kirganligini tekshirish

```html
{% if user.is_authenticated %}
    <a href="{% url 'news_create' %}" class="btn btn-primary">Yangilik qo'shish</a>
{% else %}
    <p>Yangilik qo'shish uchun <a href="{% url 'login' %}">tizimga kiring</a></p>
{% endif %}
```

### 6.2. Muallif ekanligini tekshirish

```html
{% if user == news.author or user.is_superuser %}
    <a href="{% url 'news_update' news.pk %}" class="btn btn-warning">Tahrirlash</a>
    <a href="{% url 'news_delete' news.pk %}" class="btn btn-danger">O'chirish</a>
{% endif %}
```

### 6.3. Murakkab tekshirishlar

```html
{% if user.is_authenticated %}
    {% if user == news.author %}
        <div class="alert alert-info">
            <p>Bu sizning yangiligingiz</p>
            <a href="{% url 'news_update' news.pk %}" class="btn btn-sm btn-warning">Tahrirlash</a>
            <a href="{% url 'news_delete' news.pk %}" class="btn btn-sm btn-danger">O'chirish</a>
        </div>
    {% elif user.is_staff %}
        <div class="alert alert-warning">
            <p>Siz staff foydalanuvchisiz</p>
            <a href="{% url 'news_update' news.pk %}" class="btn btn-sm btn-warning">Tahrirlash</a>
        </div>
    {% endif %}
{% endif %}
```

### 6.4. Permission'larni tekshirish

```html
{% if perms.news.add_news %}
    <a href="{% url 'news_create' %}" class="btn btn-primary">Yangilik qo'shish</a>
{% endif %}

{% if perms.news.change_news and user == news.author %}
    <a href="{% url 'news_update' news.pk %}" class="btn btn-warning">Tahrirlash</a>
{% endif %}

{% if perms.news.delete_news %}
    <a href="{% url 'news_delete' news.pk %}" class="btn btn-danger">O'chirish</a>
{% endif %}
```

---

## 7. To'liq misol: CRUD operatsiyalari

### 7.1. models.py

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class News(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Qoralama'),
        ('published', 'Nashr etilgan'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    publish_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ['-publish_time']
```

### 7.2. views.py (Class-Based Views)

```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import News, Category
from .forms import NewsForm

class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return News.objects.filter(status='published')

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'

class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/create.html'
    login_url = '/accounts/login/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_superuser

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news_list')
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_superuser
```

### 7.3. views.py (Function-Based Views)

```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import News, Category
from .forms import NewsForm

def news_list(request):
    news_list = News.objects.filter(status='published')
    return render(request, 'news/list.html', {'news_list': news_list})

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news/detail.html', {'news': news})

@login_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_detail', slug=news.slug)
    else:
        form = NewsForm()
    
    return render(request, 'news/create.html', {'form': form})

@login_required
def news_update(request, slug):
    news = get_object_or_404(News, slug=slug)
    
    # Ruxsat tekshiruvi
    if request.user != news.author and not request.user.is_superuser:
        return HttpResponseForbidden("Sizda bu yangilikni tahrirlash huquqi yo'q!")
    
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', slug=news.slug)
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'news/update.html', {'form': form, 'news': news})

@login_required
def news_delete(request, slug):
    news = get_object_or_404(News, slug=slug)
    
    # Ruxsat tekshiruvi
    if request.user != news.author and not request.user.is_superuser:
        return HttpResponseForbidden("Sizda bu yangilikni o'chirish huquqi yo'q!")
    
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    
    return render(request, 'news/delete.html', {'news': news})
```

### 7.4. urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('create/', views.NewsCreateView.as_view(), name='news_create'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('<slug:slug>/update/', views.NewsUpdateView.as_view(), name='news_update'),
    path('<slug:slug>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
]
```

---

## 8. Xavfsizlik bo'yicha maslahatlar

### 8.1. CSRF himoyasi

Django avtomatik ravishda CSRF himoyasini ta'minlaydi. Formalarni ishlatishda doim `{% csrf_token %}` qo'shishni unutmang:

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Saqlash</button>
</form>
```

### 8.2. SQL Injection'dan himoya

Django ORM avtomatik ravishda SQL Injection'dan himoya qiladi. Raw SQL ishlatishdan saqlaning:

```python
# Noto'g'ri - SQL Injection xavfi
News.objects.raw(f"SELECT * FROM news WHERE id = {user_input}")

# To'g'ri - parametrlangan so'rov
News.objects.raw("SELECT * FROM news WHERE id = %s", [user_input])

# Eng yaxshisi - ORM ishlatish
News.objects.filter(id=user_input)
```

### 8.3. XSS (Cross-Site Scripting)dan himoya

Django template'lar avtomatik ravishda HTML'ni escape qiladi:

```html
<!-- Django avtomatik escape qiladi -->
<p>{{ news.body }}</p>

<!-- Agar HTML kerak bo'lsa (ehtiyotkorlik bilan) -->
<p>{{ news.body|safe }}</p>
```

### 8.4. Parollarni xavfsiz saqlash

Django parollarni avtomatik ravishda hash qiladi. Hech qachon oddiy matn parollarini saqlamang:

```python
from django.contrib.auth.models import User

# To'g'ri
user = User.objects.create_user('username', 'email@example.com', 'password')

# Noto'g'ri
user = User(username='username', password='password')  # Hash qilinmagan!
user.save()
```

---

## 9. Best Practices

### 9.1. Mixin'lar tartibini to'g'ri joylashtirish

```python
# To'g'ri tartib
class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass

# Noto'g'ri tartib
class NewsUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    pass
```

**Qoida:** Mixin'lar chapdan o'ngga bajariladi. Avval autentifikatsiya, keyin ruxsatlar, keyin asos view.

### 9.2. DRY (Don't Repeat Yourself)

Takrorlanuvchi kodlarni custom mixin yoki dekoratorlarga ajrating:

```python
# Takrorlanish
class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().author

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user == self.get_object().author

# DRY yondashuvi
class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author

class NewsUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    pass

class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    pass
```

### 9.3. Xato xabarlarini to'g'ri ko'rsatish

Foydalanuvchilarga tushunarli xato xabarlarini ko'rsating:

```python
from django.contrib import messages
from django.shortcuts import redirect

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body', 'category']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author
    
    def handle_no_permission(self):
        messages.error(self.request, "Sizda bu yangilikni tahrirlash huquqi yo'q!")
        return redirect('news_detail', slug=self.get_object().slug)
```

### 9.4. Logging qo'shish

Ruxsat berilmagan urinishlarni log qiling:

```python
import logging

logger = logging.getLogger(__name__)

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'body']
    template_name = 'news/update.html'
    
    def test_func(self):
        news = self.get_object()
        has_permission = self.request.user == news.author
        
        if not has_permission:
            logger.warning(
                f"User {self.request.user.username} tried to update news {news.pk} "
                f"without permission"
            )
        
        return has_permission
```

### 9.5. Test yozish

Ruxsatnomalar uchun testlar yozing:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import News, Category

class NewsPermissionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('user1', 'user1@example.com', 'pass123')
        self.user2 = User.objects.create_user('user2', 'user2@example.com', 'pass123')
        self.category = Category.objects.create(name='Test', slug='test')
        self.news = News.objects.create(
            title='Test News',
            slug='test-news',
            body='Test body',
            category=self.category,
            author=self.user1
        )
    
    def test_author_can_update(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(f'/news/{self.news.slug}/update/')
        self.assertEqual(response.status_code, 200)
    
    def test_non_author_cannot_update(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.get(f'/news/{self.news.slug}/update/')
        self.assertEqual(response.status_code, 403)
    
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(f'/news/{self.news.slug}/update/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
```

---

## 10. Xulosa

Ushbu darsda biz quyidagilarni o'rgandik:

### UserPassesTestMixin
- Class-based view'larda maxsus shartlarni tekshirish
- `test_func()` metodini yozish
- Murakkab shartlarni tekshirish

### Admin panelni ochish
- Custom AdminSite yaratish
- Barcha foydalanuvchilar uchun admin panel
- Foydalanuvchilarga faqat o'z ma'lumotlarini ko'rsatish

### Dekoratorli ruxsatnomalar
- `@login_required` - autentifikatsiya tekshiruvi
- `@user_passes_test` - maxsus shartlar
- `@permission_required` - Django permission'lari
- Custom dekoratorlar yaratish

### Best Practices
- Mixin'lar tartibini to'g'ri joylashtirish
- DRY printsipiga amal qilish
- Xato xabarlarini to'g'ri ko'rsatish
- Logging qo'shish
- Testlar yozish

Keyingi darsda biz Django'da izohlar tizimini yaratishni o'rganamiz!