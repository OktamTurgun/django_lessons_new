# Lesson 12: Amaliy mashq - Database dizaynini yaratish (DrawSQL.app)

## Mashq 1: DrawSQL.app bilan tanishish

### Vazifa 1.1: Ro'yxatdan o'tish
1. `https://drawsql.app` saytiga kiring
2. "Sign up" orqali ro'yxatdan o'ting yoki "Sign in with Google" dan foydalaning
3. Dashboard'ni o'rganing va screenshot oling
4. "New Diagram" tugmasini toping

**Texnik talablar:**
- Haqiqiy email manzil ishlatish
- Xavfsiz parol o'ylab topish
- Profile ma'lumotlarini to'ldirish

### Vazifa 1.2: Interface bilan tanishish
Dashboard'da quyidagi elementlarni toping va vazifalarini yozing:

1. **"New Diagram"** tugmasi - ...
2. **"Templates"** bo'limi - ...
3. **"Recent"** bo'limi - ...
4. **"Shared with me"** bo'limi - ...
5. **Settings** - ...

### Vazifa 1.3: Template'larni o'rganish
1. "Templates" bo'limiga kiring
2. Kamida 3 ta template'ni ko'ring:
   - E-commerce
   - Blog/CMS
   - Social Media
3. Har birining strukturasini tahlil qiling va yozing

## Mashq 2: Yangi diagramma yaratish

### Vazifa 2.1: Loyiha yaratish
1. "New Diagram" tugmasini bosing
2. Quyidagi ma'lumotlarni kiriting:
   - **Name:** "News Website Database Design"
   - **Database:** PostgreSQL
   - **Description:** "Yangiliklar sayti uchun database schema"

### Vazifa 2.2: Interface elementlari
Diagramma interfeysi'da quyidagi elementlarni toping:

1. **Add Table** tugmasi
2. **Save** funksiyasi
3. **Export** bo'limi
4. **Share** tugmasi
5. **Zoom** boshqaruvi

Screenshot oling va har bir elementni belgilang.

## Mashq 3: Users jadvali yaratish

### Vazifa 3.1: Users jadvalini qurish
1. "Add Table" tugmasini bosing
2. Jadval nomini `users` qiling
3. Quyidagi maydonlarni qo'shing:

| Field name | Data type | Constraints | Default |
|------------|-----------|-------------|---------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | - |
| username | VARCHAR(50) | UNIQUE, NOT NULL | - |
| email | VARCHAR(100) | UNIQUE, NOT NULL | - |
| password | VARCHAR(255) | NOT NULL | - |
| first_name | VARCHAR(50) | - | - |
| last_name | VARCHAR(50) | - | - |
| is_active | BOOLEAN | NOT NULL | TRUE |
| is_staff | BOOLEAN | NOT NULL | FALSE |
| is_superuser | BOOLEAN | NOT NULL | FALSE |
| date_joined | TIMESTAMP | NOT NULL | NOW() |
| last_login | TIMESTAMP | NULLABLE | - |

### Vazifa 3.2: Maydonlarni sozlash
Har bir maydon uchun:
1. **Data type** to'g'ri tanlanganligini tekshiring
2. **Constraints** (cheklovlar) ni qo'shing
3. **Default values** ni o'rnating
4. **Primary Key** ni belgilang

## Mashq 4: Categories jadvali yaratish

### Vazifa 4.1: Categories jadvalini yaratish
Yangi jadval yarating va quyidagi tuzilishni hosil qiling:

```sql
categories
├── id (INTEGER, PRIMARY KEY, AUTO INCREMENT)
├── name (VARCHAR(100), UNIQUE, NOT NULL)
├── slug (VARCHAR(100), UNIQUE, NOT NULL)
├── description (TEXT, NULLABLE)
├── is_active (BOOLEAN, NOT NULL, DEFAULT: TRUE)
├── created_at (TIMESTAMP, NOT NULL, DEFAULT: NOW())
└── updated_at (TIMESTAMP, NOT NULL, DEFAULT: NOW())
```

### Vazifa 4.2: Maydon tafsilotlari
Har bir maydon uchun quyidagilarni belgilang:
1. **name** - kategoriya nomi (masalan: "Sport", "Siyosat")
2. **slug** - URL uchun (masalan: "sport", "siyosat")  
3. **description** - kategoriya tavsifi
4. **is_active** - kategoriya faol/nofaol
5. Vaqt maydonlari avtomatik to'ldirilishi

## Mashq 5: Articles jadvali yaratish

### Vazifa 5.1: Articles jadvalining asosiy tuzilishi
Eng muhim jadval bo'lgan `articles` ni yarating:

| Maydon | Tur | Cheklovlar | Izoh |
|--------|-----|------------|------|
| id | INTEGER | PK, AUTO INCREMENT | Birlamchi kalit |
| title | VARCHAR(200) | NOT NULL | Maqola sarlavhasi |
| slug | VARCHAR(200) | UNIQUE, NOT NULL | URL slug |
| content | TEXT | NOT NULL | Maqola matni |
| excerpt | TEXT | NULLABLE | Qisqa tavsif |
| featured_image | VARCHAR(500) | NULLABLE | Rasm URL |
| is_published | BOOLEAN | DEFAULT: FALSE | Nashr qilingan |
| is_featured | BOOLEAN | DEFAULT: FALSE | Tanlangan maqola |
| views_count | INTEGER | DEFAULT: 0 | Ko'rishlar soni |
| created_at | TIMESTAMP | DEFAULT: NOW() | Yaratilgan vaqt |
| updated_at | TIMESTAMP | DEFAULT: NOW() | Yangilangan vaqt |
| published_at | TIMESTAMP | NULLABLE | Nashr vaqti |

### Vazifa 5.2: Foreign Key maydonlar qo'shish
Articles jadvaliga bog'lanish uchun maydonlar qo'shing:
1. **author_id** (INTEGER, NOT NULL) - Users jadvaliga bog'lanish
2. **category_id** (INTEGER, NOT NULL) - Categories jadvaliga bog'lanish

*Eslatma: Hozircha Foreign Key bog'lanishlarini qo'shmang, keyingi qadam'da qilamiz.*

## Mashq 6: Comments va Tags jadvallari

### Vazifa 6.1: Comments jadvali
`comments` jadvalini yarating:

```
comments
├── id (PRIMARY KEY)
├── content (TEXT, NOT NULL)
├── is_approved (BOOLEAN, DEFAULT: FALSE)
├── user_id (INTEGER, NOT NULL) -> users.id
├── article_id (INTEGER, NOT NULL) -> articles.id
├── parent_id (INTEGER, NULLABLE) -> comments.id (replies uchun)
├── created_at (TIMESTAMP, DEFAULT: NOW())
└── updated_at (TIMESTAMP, DEFAULT: NOW())
```

### Vazifa 6.2: Tags jadvali
`tags` jadvalini yarating:

```
tags
├── id (PRIMARY KEY)
├── name (VARCHAR(50), UNIQUE, NOT NULL)
├── slug (VARCHAR(50), UNIQUE, NOT NULL)
├── color (VARCHAR(7), DEFAULT: '#007bff') -> HEX rang kodi
└── created_at (TIMESTAMP, DEFAULT: NOW())
```

### Vazifa 6.3: Article_Tags jadvali (Many-to-Many)
`article_tags` jadvalini yarating:

```
article_tags
├── id (PRIMARY KEY)
├── article_id (INTEGER, NOT NULL) -> articles.id
├── tag_id (INTEGER, NOT NULL) -> tags.id
└── created_at (TIMESTAMP, DEFAULT: NOW())

UNIQUE constraint: (article_id, tag_id)
```

## Mashq 7: Relationships (Bog'lanishlar) yaratish

### Vazifa 7.1: One-to-Many bog'lanishlar
DrawSQL'da quyidagi bog'lanishlarni yarating:

1. **users (1) -> articles (N)**
   - `users.id` ↔ `articles.author_id`
   - Delete action: CASCADE yoki RESTRICT

2. **categories (1) -> articles (N)**
   - `categories.id` ↔ `articles.category_id`
   - Delete action: RESTRICT

3. **users (1) -> comments (N)**
   - `users.id` ↔ `comments.user_id`
   - Delete action: CASCADE

4. **articles (1) -> comments (N)**
   - `articles.id` ↔ `comments.article_id`
   - Delete action: CASCADE

### Vazifa 7.2: Self-Referencing bog'lanish
1. **comments (1) -> comments (N)** (replies uchun)
   - `comments.id` ↔ `comments.parent_id`
   - Delete action: CASCADE

### Vazifa 7.3: Many-to-Many bog'lanish
`article_tags` orqali:
1. **articles (N) -> article_tags (N)**
   - `articles.id` ↔ `article_tags.article_id`
   
2. **tags (N) -> article_tags (N)**
   - `tags.id` ↔ `article_tags.tag_id`

### Vazifa 7.4: Bog'lanishlarni tekshirish
Har bir bog'lanish uchun quyidagilarni tekshiring:
- [ ] To'g'ri jadvallar bog'langan
- [ ] Foreign Key maydonlari aniqlangan
- [ ] Delete action sozlangan
- [ ] Relationship type to'g'ri (1:N, N:N)

## Mashq 8: Diagrammani bezash va tartibga solish

### Vazifa 8.1: Jadvallarni joylashtirish
1. Jadvallarni mantiqiy tartibda joylashtiring:
   - **Yuqori qator:** users, categories, tags
   - **O'rta qator:** articles
   - **Pastki qator:** comments, article_tags

### Vazifa 8.2: Ranglar berish
Har bir jadval turiga rang bering:
- **users:** Ko'k rang (#007bff)
- **categories:** Yashil rang (#28a745)
- **articles:** Qizil rang (#dc3545)
- **comments:** Pushti rang (#e83e8c)
- **tags:** Sariq rang (#ffc107)
- **article_tags:** Kulrang rang (#6c757d)

### Vazifa 8.3: Izohlar qo'shish
Murakkab bog'lanishlar uchun izoh qo'shing:
1. **parent_id** uchun: "Self-reference for nested comments"
2. **article_tags** uchun: "Many-to-many relationship between articles and tags