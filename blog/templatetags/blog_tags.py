from ..models import *
from django import template
from django.db.models import Min, Max
from django.db.models import Count


register = template.Library()


@register.simple_tag()
def number_book():
    return Book.objects.count()


@register.simple_tag()
def number_comment():
    return Comment.objects.count()


@register.simple_tag()
def last_book():
    return Book.objects.last()


@register.simple_tag()
def active_admin():
    admin = User.objects.annotate(book_count=Count('user_book')).order_by('-user_book').first()
    return admin


@register.simple_tag()
def active_publisher():
    publisher = Book.objects.values('publisher').annotate(book_count=Count('id')).order_by('-book_count').first()
    return publisher


@register.simple_tag()
def most_popular_books(count=3):
    return Book.objects.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]
