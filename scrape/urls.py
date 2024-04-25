from django.urls import path
from django.views.generic.base import TemplateView

from scrape.views import fetch_news

urlpatterns = [
    path('news/', TemplateView.as_view(template_name='news.html', extra_context={'title': 'News'}), name='news'),
    path('fetch_news/', fetch_news, name='fetch_news'),
    path('zomato/', TemplateView.as_view(template_name='zomato.html', extra_context={'title': 'Zomato'}), name='zomato')
]
