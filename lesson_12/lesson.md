# Lesson 12: Database dizaynini yaratish (DrawSQL.app)

## Maqsad
Ushbu darsda siz o'rganasiz:
- Ma'lumotlar bazasi dizayni nima va nima uchun muhim
- DrawSQL.app platformasi bilan tanishish
- Yangiliklar sayti uchun database schema yaratish
- Jadvallar orasidagi bog'lanishlarni belgilash
- ER-diagramma yaratish va eksport qilish

## 1. Database dizayni asoslari

### Ma'lumotlar bazasi dizayni nima?
Database dizayni - bu ma'lumotlarni qanday saqlanishi, tashkil etilishi va bir-biri bilan bog'lanishini rejalashtirish jarayoni.

### Nima uchun muhim?

**Yaxshi dizayn:**
- ✅ Ma'lumotlar takrorlanmaydi (normalizatsiya)
- ✅ Tezkor qidirish va yangilash
- ✅ Ma'lumotlar yaxlitligi saqlanadi
- ✅ Kelajakda kengaytirish oson

**Yomon dizayn:**
- ❌ Ma'lumotlar takrorlanadi
- ❌ Sekin ishlaydi
- ✅ Xatolar ko'p
- ❌ O'zgartirishlar qiyin

### Asosiy tushunchalar

#### Jadval (Table)
Ma'lumotlarni saqlash uchun struktura:
```
Users jadvali:
+----+----------+------------------+----------+
| id | username | email            | password |
+----+----------+------------------+----------+
| 1  | admin    | admin@news.com   | hash123  |
| 2  | john     | john@example.com | hash456  |
+----+----------+------------------+----------+
```

#### Maydon (Field/Column)
Jadvalning ustuni, ma'lum turdagi ma'lumot saqlaydi.

#### Yozuv (Record/Row)
Jadvalning qatori, bitta obyekt haqidagi to'liq ma'lumot.

#### Birlamchi kalit (Primary Key)
Har bir yozuvni noyob identifikatsiya qiluvchi maydon (odatda `id`).

#### Tashqi kalit (Foreign Key)
Boshqa jadvaldagi yozuvga havola qiluvchi maydon.

## 2. DrawSQL.app bilan tanishish

### DrawSQL nima?
DrawSQL - bu veb-brauzer orqali database diagrammalarini yaratish uchun bepul vosita.

**Afzalliklari:**
- 🌐 Veb-based (yuklab olish shart emas)
- 🆓 Bepul foydalanish
- 🎨 Intuitive interfeys
- 📤 Turli formatda eksport
- 🔗 SQL kod generatsiyasi

### DrawSQL.app ga ro'yxatdan o'tish

1. **Saytga kirish:**
   - `https://drawsql.app` ga kiring
   - "Sign up" tugmasini bosing

2. **Ro'yxatdan o'tish:**
   - Email manzil kiriting
   - Parol yarating
   - Yoki Google/GitHub orqali kirish

3. **Dashboard:**
   - Yangi diagramma yaratish uchun "New Diagram"
   - Template'lar ko'rish
   - Mavjud loyihalar

## 3. Yangiliklar sayti uchun database schema

### Kerakli jadvallar tahlili

Yangiliklar sayti uchun quyidagi jadvallar kerak:

1. **Users** - Foydalanuvchilar
2. **Categories** - Kategoriyalar
3. **Articles** - Maqolalar
4. **Comments** - Izohlar
5. **Tags** - Teglar
6. **Article_Tags** - Maqola va teg bog'lanishi

### Jadvallar tafsiloti

#### 1. Users jadvali
```sql
Users
├── id (Primary Key, Integer, Auto Increment)
├── username (Varchar(50), Unique, Not Null)
├── email (Varchar(100), Unique, Not Null)
├── password (Varchar(255), Not Null)
├── first_name (Varchar(50))
├── last_name (Varchar(50))
├── is_active (Boolean, Default: True)
├── is_staff (Boolean, Default: False)
├── is_superuser (Boolean, Default: False)
├── date_joined (DateTime, Default: Now)
└── last_login (DateTime, Nullable)
```

#### 2. Categories jadvali
```sql
Categories
├── id (Primary Key, Integer, Auto Increment)
├── name (Varchar(100), Unique, Not Null)
├── slug (Varchar(100), Unique, Not Null)
├── description (Text, Nullable)
├── is_active (Boolean, Default: True)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Auto Update)
```

#### 3. Articles jadvali
```sql
Articles
├── id (Primary Key, Integer, Auto Increment)
├── title (Varchar(200), Not Null)
├── slug (Varchar(200), Unique, Not Null)
├── content (Text, Not Null)
├── excerpt (Text, Nullable)
├── featured_image (Varchar(500), Nullable)
├── is_published (Boolean, Default: False)
├── is_featured (Boolean, Default: False)
├── views_count (Integer, Default: 0)
├── author_id (Foreign Key -> Users.id, Not Null)
├── category_id (Foreign Key -> Categories.id, Not Null)
├── created_at (DateTime, Default: Now)
├── updated_at (DateTime, Auto Update)
└── published_at (DateTime, Nullable)
```

#### 4. Comments jadvali
```sql
Comments
├── id (Primary Key, Integer, Auto Increment)
├── content (Text, Not Null)
├── is_approved (Boolean, Default: False)
├── user_id (Foreign Key -> Users.id, Not Null)
├── article_id (Foreign Key -> Articles.id, Not Null)
├── parent_id (Foreign Key -> Comments.id, Nullable)
├── created_at (DateTime, Default: Now)
└── updated_at (DateTime, Auto Update)
```

#### 5. Tags jadvali
```sql
Tags
├── id (Primary Key, Integer, Auto Increment)
├── name (Varchar(50), Unique, Not Null)
├── slug (Varchar(50), Unique, Not Null)
├── color (Varchar(7), Default: '#007bff')
└── created_at (DateTime, Default: Now)
```

#### 6. Article_Tags jadvali (Many-to-Many)
```sql
Article_Tags
├── id (Primary Key, Integer, Auto Increment)
├── article_id (Foreign Key -> Articles.id, Not Null)
├── tag_id (Foreign Key -> Tags.id, Not Null)
└── created_at (DateTime, Default: Now)

Unique constraint: (article_id, tag_id)
```

## 4. DrawSQL da diagramma yaratish

### Qadam 1: Yangi loyiha yaratish
1. DrawSQL dashboard'da "New Diagram" bosing
2. Loyiha nomini kiriting: "News Website Database"
3. Ma'lumotlar bazasi turini tanlang: "PostgreSQL" (yoki "MySQL")

### Qadam 2: Jadvallarni yaratish

#### Users jadvalini yaratish:
1. "Add Table" tugmasini bosing
2. Jadval nomi: `users`
3. Maydonlarni qo'shing:
   ```
   id - INTEGER, PRIMARY KEY, AUTO INCREMENT
   username - VARCHAR(50), UNIQUE, NOT NULL
   email - VARCHAR(100), UNIQUE, NOT NULL
   password - VARCHAR(255), NOT NULL
   first_name - VARCHAR(50)
   last_name - VARCHAR(50)
   is_active - BOOLEAN, DEFAULT true
   is_staff - BOOLEAN, DEFAULT false
   is_superuser - BOOLEAN, DEFAULT false
   date_joined - TIMESTAMP, DEFAULT NOW()
   last_login - TIMESTAMP
   ```

#### Categories jadvalini yaratish:
1. Yangi jadval qo'shing: `categories`
2. Maydonlar:
   ```
   id - INTEGER, PRIMARY KEY, AUTO INCREMENT
   name - VARCHAR(100), UNIQUE, NOT NULL
   slug - VARCHAR(100), UNIQUE, NOT NULL
   description - TEXT
   is_active - BOOLEAN, DEFAULT true
   created_at - TIMESTAMP, DEFAULT NOW()
   updated_at - TIMESTAMP, DEFAULT NOW()
   ```

#### Articles jadvalini yaratish:
1. Yangi jadval: `articles`
2. Maydonlar:
   ```
   id - INTEGER, PRIMARY KEY, AUTO INCREMENT
   title - VARCHAR(200), NOT NULL
   slug - VARCHAR(200), UNIQUE, NOT NULL
   content - TEXT, NOT NULL
   excerpt - TEXT
   featured_image - VARCHAR(500)
   is_published - BOOLEAN, DEFAULT false
   is_featured - BOOLEAN, DEFAULT false
   views_count - INTEGER, DEFAULT 0
   author_id - INTEGER, NOT NULL
   category_id - INTEGER, NOT NULL
   created_at - TIMESTAMP, DEFAULT NOW()
   updated_at - TIMESTAMP, DEFAULT NOW()
   published_at - TIMESTAMP
   ```

#### Comments jadvalini yaratish:
1. Yangi jadval: `comments`
2. Maydonlar:
   ```
   id - INTEGER, PRIMARY KEY, AUTO INCREMENT
   content - TEXT, NOT NULL
   is_approved - BOOLEAN, DEFAULT false
   user_id - INTEGER, NOT NULL
   article_id - INTEGER, NOT NULL
   parent_id - INTEGER
   created_at - TIMESTAMP, DEFAULT NOW()
   updated_at - TIMESTAMP, DEFAULT NOW()
   ```

#### Tags jadvalini yaratish:
1. Yangi jadval: `tags`
2. Maydonlar:
   ```
   id - INTEGER, PRIMARY KEY, AUTO INCREMENT
   name - VARCHAR(50), UNIQUE, NOT NULL
   slug - VARCHAR(50), UNIQUE, NOT NULL
   color - VARCHAR(7), DEFAULT '#007bff'
   created_at - TIMESTAMP, DEFAULT NOW()
   ```

#### Article_Tags jadvalini yaratish:
1. Yangi jadval: `article_tags`
2. Maydonlar:
   ```
   id - INTEGER, PRIMARY KEY, AUTO INCREMENT
   article_id - INTEGER, NOT NULL
   tag_id - INTEGER, NOT NULL
   created_at - TIMESTAMP, DEFAULT NOW()
   ```

### Qadam 3: Bog'lanishlar (Relationships) yaratish

#### Foreign Key bog'lanishlar:

1. **Articles -> Users (author_id)**
   - `articles.author_id` → `users.id`
   - Relationship type: Many-to-One
   - Delete action: CASCADE yoki RESTRICT

2. **Articles -> Categories (category_id)**
   - `articles.category_id` → `categories.id`
   - Relationship type: Many-to-One
   - Delete action: RESTRICT

3. **Comments -> Users (user_id)**
   - `comments.user_id` → `users.id`
   - Relationship type: Many-to-One
   - Delete action: CASCADE

4. **Comments -> Articles (article_id)**
   - `comments.article_id` → `articles.id`
   - Relationship type: Many-to-One
   - Delete action: CASCADE

5. **Comments -> Comments (parent_id) - Self Reference**
   - `comments.parent_id` → `comments.id`
   - Relationship type: One-to-Many (Self)
   - Delete action: CASCADE

6. **Article_Tags -> Articles (article_id)**
   - `article_tags.article_id` → `articles.id`
   - Relationship type: Many-to-One
   - Delete action: CASCADE

7. **Article_Tags -> Tags (tag_id)**
   - `article_tags.tag_id` → `tags.id`
   - Relationship type: Many-to-One
   - Delete action: CASCADE

### Qadam 4: Diagrammani bezash

1. **Jadvallarni joylash:**
   - Jadvallarni mantiqiy tartibda joylashtiring
   - Bog'lanish chiziqlari aniq ko'rinishi uchun

2. **Ranglar berish:**
   - Har xil turdagi jadvallarga ranglar bering
   - Users - ko'k
   - Articles - yashil
   - Categories - sariq
   - Comments - pushti

3. **Izohlar qo'shish:**
   - Murakkab bog'lanishlar uchun izoh qo'shing

## 5. SQL kodi generatsiya qilish

### DrawSQL dan SQL eksport qilish:
1. "Export" tugmasini bosing
2. "SQL" formatini tanlang
3. Ma'lumotlar bazasi turini tanlang (PostgreSQL/MySQL)
4. Kodni nusxalang yoki fayl yuklab oling

### Generatsiya qilingan SQL misoli:
```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Articles table
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt TEXT,
    featured_image VARCHAR(500),
    is_published BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    views_count INTEGER DEFAULT 0,
    author_id INTEGER NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    published_at TIMESTAMP
);

-- Boshqa jadvallar...
```

## 6. Database dizayni eng yaxshi amaliyotlar

### Nomlarni berish qoidalari:
- **Jadvallar:** ko'plik shaklda (`users`, `articles`)
- **Maydonlar:** snake_case (`first_name`, `created_at`)
- **Primary Key:** `id`
- **Foreign Key:** `table_name_id` (`author_id`, `category_id`)

### Ma'lumot turlari:
- **ID:** INTEGER/SERIAL (auto increment)
- **Matn:** VARCHAR (cheklangan) yoki TEXT (cheklanmagan)
- **Sana:** TIMESTAMP/DATETIME
- **Boolean:** BOOLEAN
- **Raqamlar:** INTEGER, DECIMAL

### Indekslar:
- Primary Key avtomatik indekslangan
- Foreign Key'larga indeks qo'shing
- Tez-tez qidiriluvchi maydonlarga indeks qo'shing

### Normalizatsiya:
- **1NF:** Har bir maydon atomik bo'lishi
- **2NF:** Qisman bog'liqlik yo'q
- **3NF:** Transitive bog'liqlik yo'q

## 7. Diagrammani saqlash va ulashish

### DrawSQL da saqlash:
1. Diagramma avtomatik saqlanadi
2. Nomi o'zgartirishingiz mumkin
3. Versiyalash imkoniyati bor

### Ulashish:
1. "Share" tugmasini bosing
2. Public havola yaratish
3. Read-only yoki edit huquqi berish

### Eksport formatlar:
- **SQL:** Database yaratish uchun
- **PNG:** Rasm shaklida
- **PDF:** Hujjat shaklida
- **SVG:** Vector grafik

## 8. Django bilan integratsiya

### Django Models kodini yaratish:

DrawSQL dan olingan SQL asosida Django modellari:

```python
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.URLField(max_length=500, blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    tags = models.ManyToManyField('Tag', through='ArticleTag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
```

## Xulosa

Ushbu darsda siz o'rgandingiz:
- Database dizayni asoslari va ahamiyati
- DrawSQL.app platformasi bilan ishlash
- Yangiliklar sayti uchun to'liq database schema
- Jadvallar orasidagi bog'lanishlar
- ER-diagramma yaratish va eksport qilish
- Django Models bilan integratsiya

Keyingi darsda biz ushbu dizaynni Django loyihasida amalga oshiramiz va real model'lar yaratamiz.