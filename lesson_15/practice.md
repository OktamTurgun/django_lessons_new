# Dars 15 - Amaliy mashg'ulot: Queryset va Model Manager

## Loyiha maqsadi
Ushbu amaliyotda biz yangiliklar sayti uchun murakkab queryset va custom manager larni yaratamiz. Blog post, kategoriya va commentlar uchun turli xil so'rovlar yaratib, performance ni optimizatsiya qilamiz.

## Bosqich 1: Modellarni tayyorlash

Dastlab, bizning asosiy modellarimizni kengaytiramiz:

### 1.1 Blog model ni yangilash

`blog/models.py` faylini oching va quyidagi kodni qo'shing:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class CategoryManager(models.Manager):
    def with_published_posts(self):
        """Faqat published postlari bor kategoriyalar"""
        return self.filter(posts__status='published').distinct()
    
    def popular(self, limit=5):
        """Eng ko'p postli kategoriyalar"""
        return self.annotate(
            post_count=models.Count('posts')
        ).order_by('-post_count')[:limit]

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Custom manager qo'shish
    objects = models.Manager()  # Standart manager
    active = CategoryManager()  # Custom manager
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class PublishedPostManager(models.Manager):
    def get_queryset(self):
        """Faqat published postlarni qaytaradi"""
        return super().get_queryset().filter(status='published')
    
    def recent(self, days=7):
        """So'nggi X kun ichida yaratilgan postlar"""
        since = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(created_at__gte=since)
    
    def by_category(self, category_name):
        """Ma'lum kategoriya bo'yicha"""
        return self.get_queryset().filter(category__name=category_name)
    
    def popular(self, limit=5):
        """Eng ko'p korilgan postlar"""
        return self.get_queryset().order_by('-views')[:limit]

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')
    
    def drafts(self):
        return self.filter(status='draft')
    
    def by_author(self, author):
        return self.filter(author=author)
    
    def search(self, query):
        return self.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query) |
            models.Q(category__name__icontains=query)
        )
    
    def with_comments(self):
        return self.annotate(
            comment_count=models.Count('comments')
        ).filter(comment_count__gt=0)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def drafts(self):
        return self.get_queryset().drafts()
    
    def search(self, query):
        return self.get_queryset().search(query)

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Managers
    objects = PostManager()           # Custom manager
    published_posts = PublishedPostManager()  # Specialized manager
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class CommentManager(models.Manager):
    def approved(self):
        return self.get_queryset().filter(approved=True)
    
    def for_post(self, post):
        return self.approved().filter(post=post)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CommentManager()
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author_name}'
```

## Bosqich 2: Migration yaratish va ma'lumot kiritish

### 2.1 Migration yaratish

Terminal da quyidagi buyruqlarni bajaring:

```bash
python manage.py makemigrations blog
python manage.py migrate
```

### 2.2 Test ma'lumotlari yaratish

`blog/management/commands/create_sample_data.py` faylini yarating:

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post, Tag, Comment
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Create sample blog data'

    def handle(self, *args, **options):
        # User yaratish
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        else:
            admin_user = User.objects.get(username='admin')

        # Kategoriyalar yaratish
        categories = [
            ('Python', 'Python dasturlash tili'),
            ('Django', 'Django web framework'),
            ('JavaScript', 'JavaScript dasturlash'),
            ('Technology', 'Texnologiya yangiliklari'),
            ('Tutorial', 'Darsliklar va qo\'llanmalar'),
        ]
        
        for name, desc in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': desc
                }
            )

        # Taglar yaratish
        tag_names = ['beginner', 'advanced', 'web', 'backend', 'frontend', 'database']
        for tag_name in tag_names:
            Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )

        # Postlar yaratish
        categories = Category.objects.all()
        tags = Tag.objects.all()
        
        post_titles = [
            'Django QuerySet optimizatsiyasi',
            'Python da OOP asoslari',
            'JavaScript ES6 yangiliklari',
            'Database indeksatsiya strategiyalari',
            'RESTful API yaratish',
            'Docker bilan deployment',
            'Git workflow best practices',
            'Testing in Django',
            'Performance monitoring',
            'Security best practices',
        ]
        
        for i, title in enumerate(post_titles):
            post = Post.objects.create(
                title=title,
                slug=slugify(title),
                content=f"Bu {title} haqida batafsil maqola. Lorem ipsum dolor sit amet consectetur adipisicing elit.",
                excerpt=f"{title} haqida qisqa ma'lumot",
                author=admin_user,
                category=random.choice(categories),
                status='published' if i < 7 else 'draft',
                views=random.randint(10, 1000),
                featured=i < 3
            )
            
            # Tasodifiy taglar qo'shish
            post.tags.set(random.sample(list(tags), random.randint(1, 3)))

        # Commentlar yaratish
        posts = Post.objects.published()
        comment_authors = ['Alisher', 'Madina', 'Bobur', 'Sevara', 'Jasur']
        
        for post in posts:
            for i in range(random.randint(0, 5)):
                Comment.objects.create(
                    post=post,
                    author_name=random.choice(comment_authors),
                    author_email=f'{random.choice(comment_authors).lower()}@example.com',
                    content=f"Bu {post.title} haqida juda yaxshi maqola!",
                    approved=True
                )

        self.stdout.write(
            self.style.SUCCESS('Sample data successfully created!')
        )
```

### 2.3 Sample data yaratish

```bash
python manage.py create_sample_data
```

## Bosqich 3: QuerySet metodlarini test qilish

### 3.1 Django shell ochish

```bash
python manage.py shell
```

### 3.2 Turli queryset larni test qilish

Shell da quyidagi kodlarni sinab ko'ring:

```python
from blog.models import Post, Category, Comment, Tag

# 1. Standart queryset operatsiyalari
print("=== Asosiy operatsiyalar ===")

# Barcha published postlar
published_posts = Post.objects.published()
print(f"Published posts: {published_posts.count()}")

# Draft postlar
draft_posts = Post.objects.drafts()
print(f"Draft posts: {draft_posts.count()}")

# 2. Custom manager metodlari
print("\n=== Custom manager metodlari ===")

# So'nggi 7 kun postlari
recent_posts = Post.published_posts.recent(7)
print(f"Recent posts: {recent_posts.count()}")

# Muayyan kategoriya postlari
python_posts = Post.published_posts.by_category('Python')
print(f"Python posts: {python_posts.count()}")

# 3. Chaining operatsiyalari
print("\n=== Chaining operatsiyalar ===")

# Bir nechta filter ni birlashtirish
complex_query = Post.objects.published().by_author(
    User.objects.get(username='admin')
).search('Django')
print(f"Complex query results: {complex_query.count()}")

# 4. Kategoriyalar bilan ishlash
print("\n=== Kategoriyalar ===")

# Published postlari bor kategoriyalar
active_categories = Category.active.with_published_posts()
print(f"Active categories: {active_categories.count()}")

# Eng popular kategoriyalar
popular_categories = Category.active.popular(3)
for cat in popular_categories:
    print(f"{cat.name}: {cat.post_count} posts")

# 5. Performance optimizatsiya
print("\n=== Performance optimizatsiya ===")

# Select related (Foreign Key optimization)
optimized_posts = Post.objects.select_related('author', 'category').published()
print("Posts with optimized author/category loading:")
for post in optimized_posts[:3]:
    print(f"- {post.title} by {post.author.username} in {post.category.name}")

# Prefetch related (Many-to-Many optimization)
posts_with_tags = Post.objects.prefetch_related('tags').published()[:3]
print("\nPosts with optimized tags loading:")
for post in posts_with_tags:
    tags = ", ".join([tag.name for tag in post.tags.all()])
    print(f"- {post.title}: [{tags}]")
```

## Bosqich 4: Views da Queryset ishlatish

### 4.1 blog/views.py ni yangilash

```python
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Post, Category, Tag

def post_list(request):
    """Postlar ro'yxati - performance optimized"""
    # Query parametrlari
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Asosiy queryset
    posts = Post.objects.published().select_related(
        'author', 'category'
    ).prefetch_related('tags')
    
    # Filtrlash
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    if search_query:
        posts = posts.search(search_query)
    
    # Annotation qo'shish
    posts = posts.annotate(
        comment_count=Count('comments', filter=Q(comments__approved=True))
    )
    
    # Pagination
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Context
    context = {
        'page_obj': page_obj,
        'categories': Category.active.with_published_posts(),
        'search_query': search_query,
        'selected_category': category_slug,
    }
    
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    """Post detali - comments bilan"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status='published'
    )
    
    # Viewsni oshirish (F expression)
    Post.objects.filter(pk=post.pk).update(
        views=models.F('views') + 1
    )
    
    # Approved comments
    comments = Comment.objects.approved().filter(post=post)
    
    # O'xshash postlar
    related_posts = Post.objects.published().filter(
        category=post.category
    ).exclude(pk=post.pk)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
    }
    
    return render(request, 'blog/post_detail.html', context)

def category_detail(request, slug):
    """Kategoriya sahifasi"""
    category = get_object_or_404(Category, slug=slug)
    
    # Kategoriya postlari
    posts = Post.objects.published().filter(
        category=category
    ).select_related('author').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistika
    stats = {
        'total_posts': posts.count(),
        'total_views': posts.aggregate(total_views=models.Sum('views'))['total_views'] or 0,
        'avg_views': posts.aggregate(avg_views=models.Avg('views'))['avg_views'] or 0,
    }
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'stats': stats,
    }
    
    return render(request, 'blog/category_detail.html', context)

def dashboard(request):
    """Admin dashboard - statistika"""
    if not request.user.is_staff:
        return redirect('post_list')
    
    # Aggregate ma'lumotlar
    stats = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.published().count(),
        'draft_posts': Post.objects.drafts().count(),
        'total_categories': Category.objects.count(),
        'total_comments': Comment.objects.count(),
        'approved_comments': Comment.objects.approved().count(),
    }
    
    # So'nggi postlar
    recent_posts = Post.objects.select_related('author', 'category')[:5]
    
    # Eng popular postlar
    popular_posts = Post.objects.published().order_by('-views')[:5]
    
    # Kategoriyalar statistikasi
    category_stats = Category.objects.annotate(
        post_count=Count('posts'),
        published_count=Count('posts', filter=Q(posts__status='published'))
    ).order_by('-post_count')
    
    context = {
        'stats': stats,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'category_stats': category_stats,
    }
    
    return render(request, 'blog/dashboard.html', context)
```

## Bosqich 5: Template larni yaratish

### 5.1 blog/templates/blog/post_list.html

```html
{% extends 'base.html' %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <div class="flex flex-wrap -mx-4">
        <!-- Sidebar -->
        <div class="w-full lg:w-1/4 px-4 mb-8">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Kategoriyalar</h3>
                <ul class="space-y-2">
                    <li>
                        <a href="{% url 'post_list' %}" 
                           class="text-blue-600 hover:text-blue-800">
                            Barcha postlar
                        </a>
                    </li>
                    {% for category in categories %}
                    <li>
                        <a href="?category={{ category.slug }}" 
                           class="text-gray-600 hover:text-gray-800
                           {% if category.slug == selected_category %}font-semibold text-blue-600{% endif %}">
                            {{ category.name }}
                        </a>
                    </li>
                    {% endfor %}
                </ul>
                
                <!-- Search form -->
                <form method="get" class="mt-6">
                    <input type="text" name="search" 
                           value="{{ search_query|default:'' }}"
                           placeholder="Qidirish..."
                           class="w-full px-3 py-2 border rounded-lg">
                    {% if selected_category %}
                        <input type="hidden" name="category" value="{{ selected_category }}">
                    {% endif %}
                    <button type="submit" 
                            class="w-full mt-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
                        Qidirish
                    </button>
                </form>
            </div>
        </div>
        
        <!-- Main content -->
        <div class="w-full lg:w-3/4 px-4">
            {% if search_query %}
                <div class="mb-4 p-4 bg-blue-50 rounded-lg">
                    <p class="text-blue-800">
                        "{{ search_query }}" uchun qidiruv natijalari: {{ page_obj.paginator.count }} ta natija
                    </p>
                </div>
            {% endif %}
            
            <div class="grid gap-6">
                {% for post in page_obj %}
                <article class="bg-white rounded-lg shadow overflow-hidden">
                    <div class="p-6">
                        <div class="flex items-center text-sm text-gray-500 mb-2">
                            <span>{{ post.author.username }}</span>
                            <span class="mx-2">•</span>
                            <span>{{ post.created_at|date:"M d, Y" }}</span>
                            <span class="mx-2">•</span>
                            <span>{{ post.category.name }}</span>
                            <span class="mx-2">•</span>
                            <span>{{ post.views }} ko'rildi</span>
                        </div>
                        
                        <h2 class="text-xl font-semibold mb-3">
                            <a href="{% url 'post_detail' post.slug %}" 
                               class="text-gray-900 hover:text-blue-600">
                                {{ post.title }}
                            </a>
                        </h2>
                        
                        <p class="text-gray-600 mb-4">{{ post.excerpt|default:post.content|truncatewords:30 }}</p>
                        
                        <div class="flex items-center justify-between">
                            <div class="flex flex-wrap gap-2">
                                {% for tag in post.tags.all %}
                                <span class="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded">
                                    {{ tag.name }}
                                </span>
                                {% endfor %}
                            </div>
                            
                            <div class="text-sm text-gray-500">
                                {{ post.comment_count }} izoh
                            </div>
                        </div>
                    </div>
                </article>
                {% empty %}
                <div class="text-center py-8">
                    <p class="text-gray-500">Hech qanday post topilmadi.</p>
                </div>
                {% endfor %}
            </div>
            
            <!-- Pagination -->
            {% if page_obj.has_other_pages %}
            <div class="mt-8 flex justify-center">
                <nav class="flex space-x-2">
                    {% if page_obj.has_previous %}
                        <a href="?page=1{% if search_query %}&search={{ search_query }}{% endif %}{% if selected_category %}&category={{ selected_category }}{% endif %}" 
                           class="px-3 py-2 bg-white border rounded hover:bg-gray-50">Birinchi</a>
                        <a href="?page={{ page_obj.previous_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if selected_category %}&category={{ selected_category }}{% endif %}" 
                           class="px-3 py-2 bg-white border rounded hover:bg-gray-50">Oldingi</a>
                    {% endif %}
                    
                    <span class="px-3 py-2 bg-blue-500 text-white border rounded">
                        {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}
                    </span>
                    
                    {% if page_obj.has_next %}
                        <a href="?page={{ page_obj.next_page_number }}{% if search_query %}&search={{ search_query }}{% endif %}{% if selected_category %}&category={{ selected_category }}{% endif %}" 
                           class="px-3 py-2 bg-white border rounded hover:bg-gray-50">Keyingi</a>
                        <a href="?page={{ page_obj.paginator.num_pages }}{% if search_query %}&search={{ search_query }}{% endif %}{% if selected_category %}&category={{ selected_category }}{% endif %}" 
                           class="px-3 py-2 bg-white border rounded hover:bg-gray-50">Oxirgi</a>
                    {% endif %}
                </nav>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### 5.2 blog/templates/blog/post_detail.html

```html
{% extends 'base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
        <!-- Post header -->
        <header class="mb-8">
            <h1 class="text-3xl font-bold mb-4">{{ post.title }}</h1>
            
            <div class="flex items-center text-gray-600 mb-4">
                <span>{{ post.author.username }}</span>
                <span class="mx-2">•</span>
                <span>{{ post.created_at|date:"F d, Y" }}</span>
                <span class="mx-2">•</span>
                <a href="{% url 'category_detail' post.category.slug %}" 
                   class="text-blue-600 hover:text-blue-800">{{ post.category.name }}</a>
                <span class="mx-2">•</span>
                <span>{{ post.views }} marta ko'rildi</span>
            </div>
            
            <!-- Tags -->
            <div class="flex flex-wrap gap-2 mb-6">
                {% for tag in post.tags.all %}
                <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                    {{ tag.name }}
                </span>
                {% endfor %}
            </div>
        </header>
        
        <!-- Post content -->
        <div class="prose max-w-none mb-8">
            {{ post.content|linebreaks }}
        </div>
        
        <!-- Related posts -->
        {% if related_posts %}
        <div class="mb-8 p-6 bg-gray-50 rounded-lg">
            <h3 class="text-lg font-semibold mb-4">O'xshash postlar</h3>
            <div class="grid md:grid-cols-3 gap-4">
                {% for related_post in related_posts %}
                <div class="bg-white p-4 rounded shadow">
                    <h4 class="font-medium mb-2">
                        <a href="{% url 'post_detail' related_post.slug %}" 
                           class="text-blue-600 hover:text-blue-800">
                            {{ related_post.title|truncatechars:50 }}
                        </a>
                    </h4>
                    <p class="text-sm text-gray-600">
                        {{ related_post.created_at|date:"M d, Y" }} • 
                        {{ related_post.views }} ko'rildi
                    </p>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <!-- Comments section -->
        <div class="border-t pt-8">
            <h3 class="text-xl font-semibold mb-6">Izohlar ({{ comments.count }})</h3>
            
            {% for comment in comments %}
            <div class="mb-6 p-4 bg-gray-50 rounded-lg">
                <div class="flex items-center justify-between mb-2">
                    <strong class="text-gray-900">{{ comment.author_name }}</strong>
                    <span class="text-sm text-gray-600">{{ comment.created_at|date:"M d, Y H:i" }}</span>
                </div>
                <p class="text-gray-700">{{ comment.content|linebreaks }}</p>
            </div>
            {% empty %}
            <p class="text-gray-500">Hali izohlar yo'q. Birinchi bo'lib izoh yozing!</p>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

## Bosqich 6: Performance Testing

### 6.1 Django Debug Toolbar o'rnatish

```bash
pip install django-debug-toolbar
```

`settings.py` ga qo'shing:

```python
INSTALLED_APPS = [
    # ... other apps
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... other middleware
]

INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_COLLAPSED': True,
}
```

### 6.2 URL konfiguratsiyasi

`urls.py` ga qo'shing:

```python
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### 6.3 Performance test scripti

`blog/management/commands/performance_test.py`:

```python
from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import Post
import time

class Command(BaseCommand):
    help = 'Test queryset performance'

    def handle(self, *args, **options):
        print("=== QuerySet Performance Test ===\n")
        
        # Test 1: N+1 Problem
        print("1. N+1 Problem Test")
        
        # Bad way - N+1 problem
        start_time = time.time()
        posts = Post.objects.published()[:10]
        for post in posts:
            print(f"Author: {post.author.username}, Category: {post.category.name}")
        bad_time = time.time() - start_time
        print(f"Bad way (N+1): {bad_time:.4f} seconds\n")
        
        # Good way - select_related
        start_time = time.time()
        posts = Post.objects.published().select_related('author', 'category')[:10]
        for post in posts:
            print(f"Author: {post.author.username}, Category: {post.category.name}")
        good_time = time.time() - start_time
        print(f"Good way (select_related): {good_time:.4f} seconds")
        print(f"Improvement: {bad_time/good_time:.2f}x faster\n")
        
        # Test 2: Many-to-Many optimization
        print("2. Many-to-Many Test")
        
        # Bad way
        start_time = time.time()
        posts = Post.objects.published()[:5]
        for post in posts:
            tags = ", ".join([tag.name for tag in post.tags.all()])
            print(f"Post: {post.title}, Tags: [{tags}]")
        bad_time = time.time() - start_time
        print(f"Bad way: {bad_time:.4f} seconds\n")
        
        # Good way - prefetch_related
        start_time = time.time()
        posts = Post.objects.published().prefetch_related('tags')[:5]
        for post in posts:
            tags = ", ".join([tag.name for tag in post.tags.all()])
            print(f"Post: {post.title}, Tags: [{tags}]")
        good_time = time.time() - start_time
        print(f"Good way (prefetch_related): {good_time:.4f} seconds")
        print(f"Improvement: {bad_time/good_time:.2f}x faster\n")
        
        # Test 3: Count vs len()
        print("3. Count vs len() Test")
        
        # len() way - loads all objects
        start_time = time.time()
        posts = Post.objects.published()
        count1 = len(posts)
        len_time = time.time() - start_time
        print(f"len() method: {count1} posts, {len_time:.4f} seconds")
        
        # count() way - database count
        start_time = time.time()
        count2 = Post.objects.published().count()
        count_time = time.time() - start_time
        print(f"count() method: {count2} posts, {count_time:.4f} seconds")
        print(f"count() is {len_time/count_time:.2f}x faster")
```

### 6.4 Performance testini ishlatish

```bash
python manage.py performance_test
```

## Bosqich 7: URL konfiguratsiyasi

### 7.1 blog/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
```

### 7.2 Asosiy urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

## Bosqich 8: Admin konfiguratsiyasi

### 8.1 blog/admin.py

```python
from django.contrib import admin
from .models import Post, Category, Tag, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'get_post_count']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_post_count(self, obj):
        return obj.posts.count()
    get_post_count.short_description = 'Posts Count'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'created_at']
    list_filter = ['status', 'category', 'created_at', 'featured']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author_name', 'approved', 'created_at']
    list_filter = ['approved', 'created_at']
    actions = ['make_approved']
    
    def make_approved(self, request, queryset):
        queryset.update(approved=True)
    make_approved.short_description = "Mark selected comments as approved"

admin.site.register(Tag)
```

## Bosqich 9: Test yozish

### 9.1 blog/tests/test_managers.py

```python
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Category, Comment

class ManagerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Published post
        self.published_post = Post.objects.create(
            title='Published Post',
            slug='published-post',
            content='This is published content',
            author=self.user,
            category=self.category,
            status='published'
        )
        
        # Draft post
        self.draft_post = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            content='This is draft content',
            author=self.user,
            category=self.category,
            status='draft'
        )

    def test_published_manager(self):
        """Test published posts manager"""
        published_posts = Post.objects.published()
        self.assertEqual(published_posts.count(), 1)
        self.assertEqual(published_posts.first(), self.published_post)

    def test_drafts_manager(self):
        """Test draft posts manager"""
        draft_posts = Post.objects.drafts()
        self.assertEqual(draft_posts.count(), 1)
        self.assertEqual(draft_posts.first(), self.draft_post)

    def test_search_functionality(self):
        """Test search functionality"""
        results = Post.objects.search('published')
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first(), self.published_post)

    def test_category_with_published_posts(self):
        """Test category manager"""
        categories = Category.active.with_published_posts()
        self.assertEqual(categories.count(), 1)
        self.assertEqual(categories.first(), self.category)
```

### 9.2 Testlarni ishlatish

```bash
python manage.py test blog.tests.test_managers
```

## Bosqich 10: Xato tuzatish va optimizatsiya

### 10.1 Database indekslar qo'shish

```python
# blog/models.py da Meta klasslariga qo'shing

class Post(models.Model):
    # ... fields ...
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['author', 'status']),
        ]

class Comment(models.Model):
    # ... fields ...
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'approved']),
        ]
```

### 10.2 Migration yaratish

```bash
python manage.py makemigrations blog
python manage.py migrate
```

## Yakuniy natija

Ushbu amaliyotda biz:

1. **Custom Manager** va **QuerySet** yaratdik
2. **Performance optimizatsiya** usullarini qo'lladik
3. **Complex queries** bilan ishladik
4. **Database indekslar** qo'shdik
5. **Testing** va **debugging** o'rnatdik

## Maslahatlar

1. **Har doim select_related** va **prefetch_related** ishlatishni unutmang
2. **Database query larni monitor** qiling (Debug Toolbar yordamida)
3. **Custom manager** nomlarini tushunarli qiling
4. **Indekslarni** to'g'ri joylashtiring
5. **Testing** yozishni unutmang

## Best Practices

- QuerySet metodlarini zanjirlab ishlating
- N+1 problemasiga e'tibor bering  
- Database level da filtrlash amalga oshiring
- Caching strategiyasini qo'llang
- Raw SQL dan faqat juda kerak bo'lganda foydalaning

Keyingi darsda biz **News list va detail page** bilan tanishamiz!