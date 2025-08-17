from django.db import models
from django.db.models.signals import post_delete
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django_resized import ResizedImageField
from django.dispatch import receiver


class Book(models.Model):
    class Genre(models.TextChoices):
        drama = 'drama', 'drama'
        sci_fi = 'sci-fi', 'sci-fi'
        romance = 'romance', 'romance'
        mystery = 'mystery', 'mystery'
        history = 'history', 'history'
        scientific = 'scientific', 'scientific'
        other = 'other', 'other'

    user_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_book')
    slug = models.SlugField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField()
    num_pages = models.PositiveIntegerField()
    author = models.CharField(max_length=250)
    publisher = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    language = models.CharField(max_length=250)
    file = models.FileField(upload_to='books/files/', blank=True, null=True)
    choices_genre = models.CharField(max_length=25, choices=Genre.choices, default=Genre.other)
    publish = models.DateField(blank=True, null=True, default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('blog:detail_book', args=[self.id])


class Ticket(models.Model):
    name = models.CharField(max_length=250)
    family = models.CharField(max_length=250)
    massage = models.TextField()
    email = models.EmailField(max_length=250)
    subject = models.CharField(max_length=250)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name


def image_upload(instance, filename):
    create_year = timezone.now().year
    return f'image_book/{create_year}/{filename}'


class Image(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    image = ResizedImageField(upload_to=image_upload, size=[350, 200], crop=['middle', 'center'], quality=85)
    created = models.DateField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=Book)
def delete_book_images(sender, instance, **kwargs):
    for image in instance.images.all():
        image.delete()


class DownloadedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloaded_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='downloads')
    downloaded_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} -> {self.book.title}"


def image_upload_account(instance, filename):
    create_year = timezone.now().year
    return f'image_account/{create_year}/{filename}'


class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    bio = models.TextField()
    birth = models.DateField(blank=True, null=True)
    job = models.CharField(blank=True, null=True)
    photos = ResizedImageField(upload_to=image_upload_account, size=[500, 500], crop=['middle', 'center'], quality=90)
    objects = models.Manager()

    def __str__(self):
        return self.user.username



