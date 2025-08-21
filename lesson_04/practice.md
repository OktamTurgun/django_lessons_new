# Lesson 04 Practice: Virtual muhitlar va Pipenv

## Maqsad
Ushbu amaliy mashqlar orqali siz:

- Virtual muhit yaratishni,
- Pipenv bilan paket o‘rnatish va boshqarishni,
- Loyihani boshqa kompyuterga ko‘chirishni

amaliyotda mustahkamlaysiz.

---

## Mashq 1: Virtual muhit yaratish

1. Yangi papka yarating, masalan:
```bash
mkdir my_first_project
cd my_first_project
```

2. Pipenv yordamida virtual muhit yarating:
```bash
pipenv install
```

3. Virtual muhitga kirish:
```bash
pipenv shell
```

4. Python versiyasini tekshiring:
```bash
python --version
```

**Kutilayotgan natija:** Terminal siz yaratgan virtual muhitda ishlayotgan bo‘lishi va Python versiyasi ko‘rinishi kerak.

---

## Mashq 2: Paket o‘rnatish va tekshirish

1. `requests` paketini o‘rnating:
```bash
pipenv install requests
```

2. O‘rnatilgan paketlarni ko‘ring:
```bash
pipenv graph
```

3. Python konsolida tekshiring:
```python
import requests
print(requests.__version__)
```

**Kutilayotgan natija:** Paket o‘rnatilgan va ishlaydi.

---

## Mashq 3: Paketni olib tashlash

1. `requests` paketini olib tashlang:
```bash
pipenv uninstall requests
```

2. Paketlar ro‘yxatini tekshiring:
```bash
pipenv graph
```

**Kutilayotgan natija:** `requests` ro‘yxatda yo‘q bo‘lishi kerak.

---

## Mashq 4: Loyihani boshqa kompyuterga ko‘chirish

1. `Pipfile` va `Pipfile.lock` fayllarini GitHub yoki boshqa kompyuterga ko‘chiring.
2. Boshqa kompyuterda virtual muhit yaratish va barcha paketlarni o‘rnatish:
```bash
pipenv install
pipenv shell
```

**Kutilayotgan natija:** Barcha kerakli paketlar o‘rnatilgan bo‘ladi va loyiha ishlaydi.

---

## Bonus Mashq: Maxsus Python versiyasini ishlatish

1. Pipenv orqali maxsus Python versiyasini o‘rnating:
```bash
pipenv --python 3.11
```

2. Virtual muhitga kirib Python versiyasini tekshiring:
```bash
pipenv shell
python --version
```

**Kutilayotgan natija:** Terminalda 3.11 versiyasi ko‘rinishi kerak.

---

## Xulosa
- Endi siz virtual muhit yaratish, paketlarni boshqarish va Pipenv asosiy buyruqlarini ishlata olasiz.
- Keyingi darsda Django loyihasini Pipenv bilan boshlashni ko‘ramiz.

