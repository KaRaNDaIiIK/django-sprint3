from django.db import models
from django.contrib.auth import get_user_model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser  # noqa


class PublishedModel(models.Model):
    """
    Абстрактная модель.
    Добвляет флаг публикации и дату создания.
    """

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        null=False
    )
    created_at = models.DateTimeField(
        'Дата добавления',
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
        verbose_name='Название',
        null=False,
        help_text='Тематическая категория, не более 256 символов'
    )
    description = models.TextField('Описание', blank=False)
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        null=False,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(PublishedModel):
    """Модель локации."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        null=False,
        help_text='Географическая метка, не более 256 символов'
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self) -> str:
        return self.name


User = get_user_model()


class Post(PublishedModel):
    """Модель поста."""

    title = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Публикация, не более 256 символов',
    )
    text = models.TextField('Описание', null=False)
    pub_date = models.DateTimeField('Дата', null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        null=False
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Локация',
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='posts',
        null=True
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        return self.title
