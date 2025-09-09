# Dars 21: ModelForm vs Form

## Dars maqsadi
Bu darsda siz Django'dagi oddiy Form va ModelForm o'rtasidagi farqlarni o'rganasiz, qachon qaysi birini ishlatish kerakligini tushunasiz va amaliy misollarda ularning afzallik va kamchiliklarini ko'rasiz.

## Nazariy qism

### Form vs ModelForm - Asosiy farqlar

| Xususiyat | Form | ModelForm |
|-----------|------|-----------|
| Ma'lumotlar bazasi bilan bog'lanish | Yo'q | Bor |
| Model bilan bog'lanish | Qo'lda | Avtomatik |
| Maydonlarni yaratish | Qo'lda | Model asosida avtomatik |
| Validatsiya | Qo'lda | Model va qo'shimcha |
| Ma'lumotlarni saqlash | Qo'lda | save() metodi bilan |
| Kodni yozish miqdori | Ko'p | Kam |

### 1. Oddiy Form (forms.Form)

Oddiy Form - ma'lumotlarni qabul qilish va qayta ishlash uchun ishlatiladi, lekin to'g'ridan-to'g'ri model bilan bog'lanmagan.

**Qachon ishlatiladi:**
- Ma'lumotlar bazasiga saqlanmaydigan ma'lumotlar uchun
- Email jo'natish, qidiruv, login kabi operatsiyalar
- Bir nechta modeldan ma'lumot to'plash kerak bo'lganda
- Murakkab validatsiya logikasi kerak bo'lganda

**Misol:**
```python
# forms.py
from django import forms

class SearchForm(forms.Form):
    """Qidiruv formasi - ma'lumotni saqlamaydi"""
    query = forms.CharField(
        max_length=200,
        label='Qidiruv so\'zi',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nima qidiryapsiz?'
        })
    )
    category = forms.ChoiceField(
        choices=[
            ('all', 'Barchasi'),
            ('news', 'Yangiliklar'),
            ('articles', 'Maqolalar'),
        ],
        label='Kategoriya',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean_query(self):
        query = self.cleaned_data.get('query')
        if len(query) < 3:
            raise forms.ValidationError('Qidiruv so\'zi kamida 3 ta belgi bo\'lishi kerak')
        return query
```

### 2. ModelForm

ModelForm - Django model asosida avtomatik yaratilgan forma. Model maydonlari asosida forma maydonlarini avtomatik yaratadi.

**Qachon ishlatiladi:**
- Model ma'lumotlarini yaratish/tahrirlash
- CRUD operatsiyalari
- Model validatsiyasidan foydalanish
- Kod yozishni minimallash

**Misol:**
```python
# models.py
from django.db import models
from django.core.validators import RegexValidator

class Contact(models.Model):
    """Bog'lanish ma'lumotlari modeli"""
    name = models.CharField(max_length=100, verbose_name='Ism-familiya')
    email = models.EmailField(verbose_name='Email manzil')
    phone = models.CharField(
        max_length=20, 
        verbose_name='Telefon raqam',
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Telefon raqam formati noto\'g\'ri'
        )]
    )
    subject = models.CharField(max_length=200, verbose_name='Mavzu')
    message = models.TextField(verbose_name='Xabar')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    is_read = models.BooleanField(default=False, verbose_name='O\'qilganmi')
    
    class Meta:
        verbose_name = 'Bog\'lanish'
        verbose_name_plural = 'Bog\'lanishlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

# forms.py
from django import forms
from .models import Contact

class ContactModelForm(forms.ModelForm):
    """Contact modeli uchun ModelForm"""
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism-familiyangizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 90 123 45 67'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xabar mavzusi'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Xabaringizni yozing...'
            })
        }
        labels = {
            'name': 'Ism-familiya',
            'email': 'Email manzil',
            'phone': 'Telefon raqam',
            'subject': 'Xabar mavzusi',
            'message': 'Xabar matni'
        }
    
    def clean_message(self):
        """Qo'shimcha validatsiya"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Xabar kamida 10 ta belgi bo\'lishi kerak')
        return message
```

## Form vs ModelForm - Amaliy misollar

### 1. Oddiy Form - Login sahifasi

```python
# forms.py
class LoginForm(forms.Form):
    """Login formasi - ma'lumotni saqlamaydi"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Foydalanuvchi nomi'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parol'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean(self):
        """Form validatsiyasi"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Username yoki parol noto\'g\'ri')
        
        return cleaned_data

# views.py
from django.contrib.auth import login
from django.shortcuts import redirect

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        
        if user:
            login(self.request, user)
            return super().form_valid(form)
        
        return self.form_invalid(form)
```

### 2. ModelForm - Yangilik yaratish

```python
# models.py
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    slug = models.SlugField(unique=True, verbose_name='URL nomi')
    content = models.TextField(verbose_name='Matn')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Muallif')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Kategoriya')
    image = models.ImageField(upload_to='news/', verbose_name='Rasm')
    published = models.BooleanField(default=False, verbose_name='Nashr etilsinmi')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# forms.py
class NewsModelForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'image', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def save(self, commit=True):
        """Qo'shimcha logika bilan saqlash"""
        news = super().save(commit=False)
        news.author = self.user  # View'dan uzatiladi
        
        if commit:
            news.save()
        return news

# views.py
from django.views.generic import CreateView

class NewsCreateView(CreateView):
    model = News
    form_class = NewsModelForm
    template_name = 'news/create.html'
    success_url = reverse_lazy('news:list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
```

## ModelForm'ning qo'shimcha imkoniyatlari

### 1. Maydonlarni cheklash

```python
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']  # Faqat kerakli maydonlar
        # yoki
        exclude = ['created_at', 'is_read']  # Bu maydonlardan tashqari barchasi
```

### 2. Custom validatsiya

```python
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Contact.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email manzil allaqachon mavjud')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        message = cleaned_data.get('message')
        
        if name and message and name.lower() in message.lower():
            raise forms.ValidationError('Xabarda ismingizni takrorlamang')
        
        return cleaned_data
```

### 3. Save metodini o'zgartirish

```python
class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
    
    def save(self, commit=True):
        contact = super().save(commit=False)
        
        # Qo'shimcha logika
        contact.name = contact.name.title()  # Ismni katta harf bilan
        
        if commit:
            contact.save()
            
            # Email jo'natish
            send_mail(
                'Yangi xabar',
                f'Sizga {contact.name} dan xabar keldi',
                'noreply@example.com',
                ['admin@example.com']
            )
        
        return contact
```

## Qachon qaysi birini ishlatish kerak?

### Form ishlatish kerak bo'lgan holatlar:

1. **Ma'lumotlarni saqlamaydigan operatsiyalar:**
```python
# Qidiruv formasi
class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
```

2. **Bir nechta model bilan ishlash:**
```python
# Foydalanuvchi profili va contact ma'lumotlarini birga o'zgartirish
class ProfileForm(forms.Form):
    # User model maydonlari
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    # Profile model maydonlari
    bio = forms.CharField(widget=forms.Textarea)
    website = forms.URLField(required=False)
```

3. **Email jo'natish formasi:**
```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    
    def send_email(self):
        # Email jo'natish logikasi
        pass
```

### ModelForm ishlatish kerak bo'lgan holatlar:

1. **CRUD operatsiyalari:**
```python
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
```

2. **Model ma'lumotlarini tahrirlash:**
```python
class NewsUpdateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category']
```

3. **Model validatsiyasidan foydalanish:**
```python
# Model'da validatsiya
class User(models.Model):
    email = models.EmailField(unique=True)  # Unique validatsiya

# ModelForm avtomatik unique validatsiyani qo'llaydi
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
```

## Hybrid yondashuv

Ba'zan Form va ModelForm'ni birlashtirish kerak:

```python
class NewsWithCategoryForm(forms.Form):
    """Yangilik va yangi kategoriya yaratish"""
    # News uchun maydonlar
    title = forms.CharField(max_length=200)
    content = forms.TextField()
    
    # Category uchun maydon
    category_name = forms.CharField(max_length=100, required=False)
    existing_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get('category_name')
        existing_category = cleaned_data.get('existing_category')
        
        if not category_name and not existing_category:
            raise forms.ValidationError('Kategoriya tanlang yoki yangi yarating')
        
        if category_name and existing_category:
            raise forms.ValidationError('Faqat bitta kategoriyan tanlang')
        
        return cleaned_data
    
    def save(self):
        # Kategoriya yaratish yoki tanlash
        if self.cleaned_data['category_name']:
            category = Category.objects.create(
                name=self.cleaned_data['category_name']
            )
        else:
            category = self.cleaned_data['existing_category']
        
        # Yangilik yaratish
        news = News.objects.create(
            title=self.cleaned_data['title'],
            content=self.cleaned_data['content'],
            category=category
        )
        
        return news
```

## Xulosa

**Form ishlatish kerak:**
- Ma'lumotlarni saqlamaydigan operatsiyalar
- Murakkab validatsiya
- Bir nechta model bilan ishlash
- To'liq nazorat kerak bo'lganda

**ModelForm ishlatish kerak:**
- CRUD operatsiyalari
- Model asosida formalar
- Kod yozishni kamaytirish
- Django'ning tayyor validatsiyalaridan foydalanish

**Keyingi dars:**
Bosh sahifada yangiliklarni kategoriya bo'yicha ko'rsatish usullarini o'rganamiz.