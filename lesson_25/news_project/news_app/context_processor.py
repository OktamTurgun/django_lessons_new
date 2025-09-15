from .models import News, Category

def latest_news(request):
    latest_news = News.published.order_by('-published_at')[:10]
    categories = Category.objects.all()

    context = {
        'latest_news': latest_news,
        'categories': categories,
    }
    return context
