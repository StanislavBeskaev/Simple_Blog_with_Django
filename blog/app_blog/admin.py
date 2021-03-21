from django.contrib import admin

from app_media.models import PostImage
from .models import Post


class PostImageInLine(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['id', 'post_author', 'post_title', 'publication_date']
    list_filter = ['publication_date']
    inlines = [PostImageInLine]
