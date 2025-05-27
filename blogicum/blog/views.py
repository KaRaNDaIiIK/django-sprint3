from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.models import Category, Post

from blogicum.settings import MAX_LEN_POST


def get_published_posts():
    """Возвращает queryset опубликованных постов."""
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).select_related('category', 'location', 'author').order_by('-pub_date')


def index(request: HttpRequest) -> HttpResponse:
    """View-функция для страницы 'Лента записей'."""
    posts = get_published_posts()[:MAX_LEN_POST]
    context = {'post_list': posts}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """View-функция для детального просмотра одной записи."""
    post_qs = get_published_posts()
    post = get_object_or_404(post_qs, pk=post_id)

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """View-функция для просмотра записей определенной категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    # Выборка повторяется выше - можно вынести в функцию
    posts = get_published_posts().filter(category=category)

    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, 'blog/category.html', context)
