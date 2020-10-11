from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STATUS_CHOICESS = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    role = models.CharField(
        max_length=15,
        choices=STATUS_CHOICESS,
        default='user'
    )
    username = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=True
    )
    rating = models.IntegerField(blank=True, null=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Review(models.Model):
   title = models.ForeignKey(
       Title,
       on_delete=models.CASCADE,
       related_name='reviews'
   )
   author = models.ForeignKey(User, on_delete=models.CASCADE)
   text = models.TextField(max_length=255)
   score = models.IntegerField(default=0)
   pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
