from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import News


# Create your views here.
def news(request):
    all_news = News.objects.all()
    s_news = News.objects.filter(selected=True)
    return render(request, 'news/list.html', {'all_news': all_news, 's_news': s_news})


def news_detail(request, pk):
    news = News.objects.get(id=pk)
    all_news = News.objects.all()[:5]
    return render(request, 'news/detail.html', {'news': news, 'all_news': all_news})
