from django.contrib import admin
from .models import Category

#___________________________________________________________________________________________
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('order',)
