from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from blog.models import Post, Category
from django.utils import timezone


def index(request: HttpRequest) -> HttpResponse:
    """View-функция для страницы 'Лента записей'."""
    template_name = 'blog/index.html'
    post = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {'post_list': post}
    return render(request, template_name, context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """View-функция для детального просмотра одной записи."""
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).select_related('category', 'location', 'author'),
        pk=post_id
    )

    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """View-функция для просмотра записей определенной категории."""
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    # Получаем опубликованные посты этой категории
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related(
        'category',
        'location',
        'author'
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, template_name, context)
