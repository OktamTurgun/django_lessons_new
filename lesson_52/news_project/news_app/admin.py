from django.contrib import admin
from .models import News, Category, Contact, Comment

# Register your models here.
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "slug", "published_at", "created_at", "category", "status")
    list_filter = ("status", "author", "category", "published_at")
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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "short_text", "created_at", "active")
    list_filter = ("active", "created_at", "author")
    search_fields = ("author__username", "text", "news__title")
    actions = ["approve_comments", "disapprove_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
    disapprove_comments.short_description = "Disapprove selected comments"

    def short_text(self, obj):
        return obj.text[:50]  # faqat birinchi 50 ta belgini chiqaradi
    short_text.short_description = "Comment"

    
