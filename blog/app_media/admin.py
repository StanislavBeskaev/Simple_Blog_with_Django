from django.contrib import admin

from .models import ProfileAvatarImage, PostImage


@admin.register(ProfileAvatarImage)
class AdminProfileAvatarImage(admin.ModelAdmin):
    list_display = ['id', 'avatar_image_file']


@admin.register(PostImage)
class AdminPostImage(admin.ModelAdmin):
    list_display = ['id', 'post_image_file', 'post']
