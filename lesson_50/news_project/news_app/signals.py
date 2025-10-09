from django.db.models.signals import post_save
from django.dispatch import receiver
from deep_translator import GoogleTranslator
from .models import News, Category

@receiver(post_save, sender=News)
def auto_translate_news(sender, instance, created, **kwargs):
    if not created:
        return

    changed = False

    try:
        print("🟢 Tarjima jarayoni boshlandi:", instance.title)
        # Title tarjimalari
        if not instance.title_en:
            instance.title_en = GoogleTranslator(source='uz', target='en').translate(instance.title)
            changed = True
        if not instance.title_ru:
            instance.title_ru = GoogleTranslator(source='uz', target='ru').translate(instance.title)
            changed = True

        # Content tarjimalari
        if not instance.content_en:
            instance.content_en = GoogleTranslator(source='uz', target='en').translate(instance.content)
            changed = True
        if not instance.content_ru:
            instance.content_ru = GoogleTranslator(source='uz', target='ru').translate(instance.content)
            changed = True

    except Exception as e:
        print(f"Tarjima xatosi: {e}")

    if changed:
        instance.save()
        print("✅ Tarjima saqlandi:", instance.title)

# --- CATEGORY TRANSLATION ---
@receiver(post_save, sender=Category)
def auto_tarnslate_category(snder, instance, created, **kwargs):
    if not created:
        return
    changed = False
    try:
        print("🟢 Tarjima jarayoni boshlandi (Category):", instance.name)

        if not instance.name_en:
            instance.name_en = GoogleTranslator(source='uz', target='en').translate(instance.name)
            changed = True
        if not instance.name_ru:
            instance.name_ru = GoogleTranslator(source='uz', target='ru').translate(instance.name)
            changed = True

    except Exception as e:
        print(f"❌ Tarjima xatosi (Category): {e}")

    if changed:
        instance.save()
        print("✅ Tarjima saqlandi (Category):", instance.name)
