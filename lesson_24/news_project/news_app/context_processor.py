from .models import News

def latest_news(request):
    latest_news = News.published.order_by('-published_at')[:10]
    context = {
        'latest_news': latest_news
    }
    return context
