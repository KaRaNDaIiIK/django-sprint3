from django.db import models
from django.contrib.auth import get_user_model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser  # noqa

User = get_user_model()


class PublishedModel(models.Model):
    """
    Абстрактная модель.
    Добвляет флаг публикации и дату создания.
    """

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        null=False,
        help_text='Снимите галочку, чтобы скрыть публикацию.'

    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
        editable=False,
        null=False,
        db_index=True)

    class Meta:
        abstract = True


class Category(PublishedModel):
    """Модель категории"""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        null=False,
        help_text='Тематическая категория, не более 256 символов'
    )
    description = models.TextField('Описание', blank=False)
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        null=False,
        db_index=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(PublishedModel):
    """Модель локации."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
        null=False,
        help_text='Географическая метка, не более 256 символов'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(PublishedModel):
    """Модель поста."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        help_text='Публикация, не более 256 символов',
    )
    text = models.TextField('Текст', null=False)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        null=False,
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_posts',
        verbose_name='Автор публикации',
        null=False
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Местоположение',
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='category_posts',
        null=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.title
