# Django Lessons New

Ushbu repository Python va Django bo'yicha mukammal darslarni o'rganish uchun mo'ljallangan. Har bir dars alohida papkada joylashgan va unda nazariy `lesson.md` va amaliy `practice.md` fayllari mavjud.

## Darslar ro'yxati
# Django Lessons New (VS Code Optimized)

Ushbu repository Python va Django bo'yicha mukammal darslarni o'rganish uchun mo'ljallangan. Har bir dars alohida papkada joylashgan va unda nazariy `lesson.md` va amaliy `practice.md` fayllari mavjud.

## Darslar ro'yxati

### Boshlang‘ich va muhityaratish
1. Django yangi versiyalar bilan ishlash
2. Terminal bilan tanishish
3. Django arxitekturasi va ishlash tamoyili
4. Virtual muhitlar bilan tanishish. Pipenv o‘rnatish va sozlash
5. VS Code dasturini sozlash va kengaytmalar o‘rnatish
6. Blog loyihasini ishga tushirish

### Asosiy Django qismlari
7. Django qismlari bilan tanishish
8. Blog model qismi
9. Blog loyihasi: Views va templates bilan ishlash
10. BlogDetail: Funksiyaga asoslangan View

### Loyihalarni yaratish va boshqarish
11. Yangiliklar sayti loyihasi bilan tanishish
12. Loyihaning starter kodini ishga tushirish va virtual muhit o‘rnatish
13. Database dizaynini yaratish (DrawSQL.app)
14. Loyiha modelini tuzish
15. Admin qismi bilan ishlash
16. Queryset va model manager
17. News list va detail page
18. Template va static fayllar bilan ishlash
19. Yangiliklar sayti shablonini Django’ga o‘rnatish

### Forms va user management
20. Home va Contact sahifalarini ishga tushirish
21. Formalar bilan ishlash: Contact Form
22. Class bilan FormView yaratish
23. ModelForm vs Form
24. Bosh sahifada yangiliklarni kategoriya bo‘yicha ko‘rsatish (1-qism)
25. Context manager bilan bosh sahifa (2-qism)
26. Context_processor va get_context_data
27. Template teglari: Loyihani to‘ldirish
28. URLni slugga o‘zgartirish: get_absolute_url
29. Yangiliklar sayti sahifasini yaratish

### Git va CRUD amaliyotlar
30. Git: Loyihani GitHub’ga yuklash
31. Yangiliklarni tahrirlash va o‘chirish funksiyalari
32. Saytga yangilik qo‘shish: CreateView

### Foydalanuvchi autentifikatsiyasi
33. Login va Logout
34. Foydalanuvchi profilini yaratish
35. Foydalanuvchi parolini o‘zgartirish
36. Foydalanuvchi parolini qayta tiklash (1-qism)
37. Foydalanuvchi parolini qayta tiklash (2-qism)

### Signup va ruxsatnomalar
38. Signup: Class View orqali ro‘yxatdan o‘tish
39. Profil modelini yaratish va tahrirlash
40. Login_required dekoratori va LoginRequiredMixin
41. Profilda rasm va boshqa ma’lumotlarni chiqarish
42. Ruxsatnomalar: LoginRequiredMixin vs UserPassesTestMixin
43. Admin sahifasi: dekoratorli ruxsatnomalar

### Izohlar va interaktivlik
44. Django’da izoh qoldirish. Izoh modeli va formasini yaratish (1-qism)
45. Views qismini yozish (2-qism)
46. Template qismini yozish (3-qism)
47. Yangiliklarni izlash funksiyasi
48. Ko‘rishlar sonini aniqlash
49. Ko‘rishlar sonini template’da aks ettirish
50. Izohlar sonini template’dan chiqarish va GitHub’ga o‘zgarishlarni saqlash

### Tarjima va internationalization
51. Veb-saytni i18n orqali tarjima qilish
52. ModelTranslation modulidan foydalanib modelni tarjima qilish
53. Template’dagi matnlarni tarjima qilish

### Deployment
54. Deployment: Ahost serveriga joylash (1-qism)
55. Deployment: Ahost serveriga joylash (2-qism)

### Testlash
56. Django uchun testlar

## Loyihaning tuzilishi
```
django_lessons_new/
├─ lesson_01/
│   ├─ lesson.md
│   └─ practice.md
├─ lesson_04/
│   ├─ lesson.md
│   ├─ practice.md
│   └─ Pipenv_project/
│       ├─ Pipfile
│       └─ Pipfile.lock
├─ django_projects_cheetsheets.md
└─ README.md
```

## Qanday ishlatish

1. Repository’ni klonlash:

```bash
git clone https://github.com/username/django_lessons_new.git
cd django_lessons_new
```

2. Virtual muhit yaratish (lesson_04 uchun):

```bash
cd lesson_04/Pipenv_project
pipenv install
pipenv shell
```

3. Har bir lesson papkasida `lesson.md` va `practice.md` fayllarni o‘rganish va amaliyot qilish.

## Litsenziya

Ushbu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil [LICENSE](LICENSE) faylga qarang.


## Muallif
**GitHub:** [OktamTurgun](https://github.com/OktamTurgun)