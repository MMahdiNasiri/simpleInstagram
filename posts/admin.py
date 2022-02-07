from django.contrib import admin

# Register your models here.
from .models import Post, Like, Comment


class PostLikeAdmin(admin.TabularInline):
    model = Like


class PostCommentAdmin(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin, PostCommentAdmin]

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)

