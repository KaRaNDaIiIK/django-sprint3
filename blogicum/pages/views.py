from django.views.generic.base import TemplateView


class AboutView(TemplateView):
    """Класс-представление для страницы 'О проекте'."""

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Класс-представление для страницы 'Наши правила'."""

    template_name = 'pages/rules.html'
