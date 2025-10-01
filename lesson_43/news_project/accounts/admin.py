from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')
    search_fields = ('user__username', 'location')
    list_filter = ('birth_date',)

admin.site.register(Profile, ProfileAdmin)