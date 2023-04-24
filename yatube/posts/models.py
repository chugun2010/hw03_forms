from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify


User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name="Текс поста",
        help_text="Введите текст поста"
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def __save__(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:15]
            super().save(*args, **kwargs)
