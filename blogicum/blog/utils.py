from django.utils import timezone


def get_published_posts():
    """Возвращает queryset опубликованных постов."""
    from blog.models import Post
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('category', 'location', 'author').order_by('-pub_date')


def trim_text(text: str, max_len: int) -> str:
    """Обрезает текст до указанного лимита символов."""
    return text[:max_len] + ('...' if len(text) > max_len else '')
