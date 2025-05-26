from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404

# TODO Удалить posts при подключении views
posts: list = []


def index(request: HttpRequest) -> HttpResponse:
    """View-функция для страницы 'Лента записей'."""
    reversed_posts = list(reversed(posts))
    context = {'posts': reversed_posts}
    return render(request, 'blog/index.html', context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """View-функция для детального просмотра одной записи."""
    try:
        post = posts[post_id]  # Получаем конкретный пост по ID
    except IndexError:
        raise Http404('Запись не найдена')
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """View-функция для просмотра записей определенной категории."""
    filtered_posts = [post for post in posts if post['category']
                      == category_slug]
    context = {
        'category': category_slug,
        'posts': filtered_posts
    }
    return render(request, 'blog/category.html', context)
