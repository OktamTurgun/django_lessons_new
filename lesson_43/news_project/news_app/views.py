from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
  ListView, 
  DetailView, 
  TemplateView, 
  CreateView, 
  UpdateView, 
  DeleteView
)
from django.views.generic.edit import FormView
from .models import News, Category
from .forms import ContactForm, NewsForm
from django.urls import reverse_lazy

# Create your views here.
# def news_list(request):
#     news = News.objects.filter(status=News.Status.PUBLISHED)
#     #news = News.published.all()
#     context = {
#         'news': news
#     }
#     return render(request, 'news/news_list.html', context)

# def news_detail(request, id):
#     news_item = get_object_or_404(News, id=id, status=News.Status.PUBLISHED)
#     context = {
#         'news_item': news_item
#     }
#     return render(request, 'news/news_detail.html', context)

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    queryset = News.published.all()
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context
    
class NewsDetailView(DetailView):
    model = News
    template_name = "news/news_deatil.html"
    context_object_name = 'news_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = News.published.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related news
        context["related_news"] = News.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        # Popular news
        context["popular_news"] = News.objects.order_by("-views")[:5]
        # Categories
        context["categories"] = Category.objects.all()
        return context
    
class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'                       
    queryset = News.published.all().order_by('-created_at')
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Slider / "latest" uchun kesma (paginationni buzmaslik uchun object_list ni o'zgartirmaymiz)
        context['news_list'] = News.published.all().order_by('-created_at')[:6]
        context['latest_news'] = News.published.order_by('-published_at')[:6] 
        context['local_news'] = News.published.filter(category__name__iexact='Mahalliy').order_by('-published_at')[:5]
        context['xorij_news'] = News.published.filter(category__name__iexact='Xorij').order_by('-published_at')[:5]
        context['sport'] = News.published.filter(category__name__iexact='Sport').order_by('-published_at')[:5]
        context['texnologiya'] = News.published.filter(category__name__iexact='Texnologiya').order_by('-published_at')[:5]
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context
    
class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

def custom_404_view(request, exception=None):
    
    return render(request, 'news/404.html', status=404)
    
class AboutPageView(TemplateView):
    template_name = 'news/about.html'

# def contactPageview(request):
#     form = ContactForm()
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = ContactForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'news/contact.html', context)

class ContactPageView(FormView):
    template_name = 'news/contact.html'
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Xabaringiz muvaffaqiyatli yuborildi!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.published.order_by('-published_at')[:10]
        context['categories'] = Category.objects.all()
        context['popular_news'] = News.published.order_by('-published_at')[:6]
        return context
    

class SinglePageView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = News.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_item = self.object

        # Related news (o‘sha kategoriyadagi boshqa yangiliklar)
        context['related_news'] = News.published.filter(
            category=news_item.category
        ).exclude(id=news_item.id)[:3]

        # Categories (sidebar uchun)
        context['categories'] = Category.objects.all()

        # Popular news (views bo‘yicha)
        context['popular_news'] = News.published.order_by('-published_at')[:4]

        # Latest news (oxirgi 10 ta)
        context['latest_news'] = News.published.order_by('-published_at')[:10]

        # Latest comments (agar comment modeli bo‘lsa)
        if hasattr(news_item, 'comments'):
            context['latest_comments'] = news_item.comments.all()[:4]
        else:
            context['latest_comments'] = []

        # Sponsor image (agar mavjud bo‘lsa)
        context['sponsor_image'] = getattr(news_item, 'sponsor_image', None)

        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = "news/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_list'] = News.published.filter(category=self.object).order_by('-published_at')
        context['categories'] = Category.objects.all()
        return context
    
class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'crud/news_create.html'
    success_url = reverse_lazy('news:home')

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'crud/news_edit.html'

    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_superuser

class NewsDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('news:home')

    def test_func(self):
        news = self.get_object()
        return self.request.user == news.author or self.request.user.is_superuser
    
def search_view(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = News.objects.filter(title__icontains=query)  # sarlavhadan qidiradi

    return render(request, "news/search_results.html", {
        "query": query,
        "results": results
    })