from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    list_display = ['user_by', 'title', 'author', 'language', 'publish']
    list_filter = ['user_by', 'language', 'choices_genre']
    ordering = ['publish']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ['title']}
    inlines = [ImageInline, CommentInline]


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    list_display = ['name', 'family', 'email', 'subject']
    list_filter = ['subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'created']
    list_filter = ['active', 'created']


@admin.register(Image)
class AdminImage(admin.ModelAdmin):
    list_display = ['name', 'book', 'created']


@admin.register(DownloadedBook)
class DownloadedBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'downloaded_at']


@admin.register(Account)
class AdminAccount(admin.ModelAdmin):
    list_display = ['user', 'bio', 'birth', 'photos', 'job']