from django.contrib import admin
from .models import News, Category, Contact

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "published_at", "created_at", "category", "status")
    list_filter = ("status", "category", "published_at")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    search_fields = ("title", "content")
    ordering = ("status", "published_at")
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
    
