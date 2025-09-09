from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from .models import News, Category
from .forms import ContactForm

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
    template_name = 'news/news_detail.html'
    context_object_name = 'news_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = News.published.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.published.filter(
            category=self.object.category,
        ).exclude(id=self.object.id)[:3]
        return context
    
class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    queryset = News.published.all()
    paginate_by = 6 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context
    
class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

def custom_404_view(request, exception):
    
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