from django.contrib import admin
from .models import Article, Comment

# Register your models here.
admin.site.register(Article)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'body', 'article__title')