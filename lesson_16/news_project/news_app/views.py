from django.shortcuts import render, get_object_or_404
from .models import News, Category

# Create your views here.
def news_list(request):
    news = News.objects.filter(status=News.Status.PUBLISHED)
    #news = News.published.all()
    context = {
        'news': news
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, id):
    news_item = get_object_or_404(News, id=id, status=News.Status.PUBLISHED)
    context = {
        'news_item': news_item
    }
    return render(request, 'news/news_detail.html', context)