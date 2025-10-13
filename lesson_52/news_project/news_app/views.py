from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
  ListView, 
  DetailView, 
  TemplateView, 
  CreateView, 
  UpdateView, 
  DeleteView
)
from django.views.generic.edit import FormView, FormMixin
from .models import News, Category
from .forms import ContactForm, NewsForm, CommentForm
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# ================================
# NewsList view - FUNCTION BASED
# ================================
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


# ================================
# NewsList view - CLASS BASED
# ================================
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
    

class SinglePageView(FormMixin, DetailView):
    model = News
    template_name = 'news/news_detail.html'
    form_class = CommentForm
    context_object_name = 'news_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = News.published.all()

    def get(self, request, *args, **kwargs):
        # obyektni olamiz
        self.object = self.get_object()

        # sessiya asosida views hisoblash
        session_key = f"viewed_news_{self.object.slug}"
        if not request.session.get(session_key, False):
            # views++ DB darajasida atomik
            News.objects.filter(slug=self.object.slug).update(views=F('views') + 1)
            request.session[session_key] = True

        # yangilangan qiymatni olish
        self.object.refresh_from_db(fields=['views'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_item = self.object

        # Related news (o'sha kategoriyadagi boshqa yangiliklar)
        context['related_news'] = News.published.filter(
            category=news_item.category
        ).exclude(id=news_item.id)[:3]

        # Categories (sidebar uchun)
        context['categories'] = Category.objects.all()

        # Popular news (views bo'yicha)
        context['popular_news'] = News.published.order_by('-published_at')[:4]

        # Latest news (oxirgi 10 ta)
        context['latest_news'] = News.published.order_by('-published_at')[:10]

        # Comments (faol kommentariyalar)
        context['comments'] = news_item.comments.filter(active=True)
        
        # Comment form - agar POST da xato bo'lsa, xatoli formani ko'rsatish
        if 'comment_form' not in context:
            context['comment_form'] = self.get_form()

        # Latest comments (agar comment modeli bo'lsa)
        if hasattr(news_item, 'comments'):
            context['latest_comments'] = news_item.comments.all()[:4]
        else:
            context['latest_comments'] = []

        # Sponsor image (agar mavjud bo'lsa)
        context['sponsor_image'] = getattr(news_item, 'sponsor_image', None)

        return context
    
    def get_success_url(self):
        return reverse_lazy('news:news_detail', kwargs={'slug': self.object.slug})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.news = self.object
        comment.save()
        messages.success(self.request, "✅ Izohingiz muvaffaqiyatli qo'shildi!")
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        """Agar forma xato bo'lsa, xatolarni ko'rsatish"""
        return self.render_to_response(
            self.get_context_data(comment_form=form)
        )

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
    
# ================================
# SEARCH VIEW - FUNCTION BASED
# ================================
def search_view(request):
    query = request.GET.get("q")
    results = News.objects.none()

    if query:
        queryset = News.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )

        # Pagination (6 ta natija per page)
        paginator = Paginator(queryset, 6)
        page_number = request.GET.get("page")
        results = paginator.get_page(page_number)

    return render(request, "news/search_results.html", {
        "query": query,
        "results": results
    })

# ================================
# SEARCH VIEW - CLASS BASED
# ================================
class SearchResultsView(ListView):
    model = News
    template_name = "news/search_results.html"
    paginate_by = 6  # bir sahifada nechta natija
    context_object_name = "object_list"  # default; keyinalgi kodda 'results' ni qo'shamiz

    def get_queryset(self):
        """
        Qidiruv so'rovini oladi va queryset qaytaradi.
        .distinct() qo'shish duplikatlarni olib tashlash uchun foydali bo'lishi mumkin
        (masalan, join natijasida takroriy yozuvlar paydo bo'lsa).
        select_related bilan author va category ni oldindan yuklash (N+1 muammosini kamaytirish)
        """
        q = self.request.GET.get("q", "").strip()
        if not q:
            # Hech qidiruv bo'lmasa bo'sh queryset qaytaramiz
            return News.objects.none()

        qs = News.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(category__name__icontains=q)
        ).select_related("category", "author").order_by("-published_at").distinct()

        # Full-Text Search
        # search_vector = SearchVector("title", "content", "category__name")
        # search_query = SearchQuery(q)

        # qs = (News.objects
        #       .annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
        #       .filter(search=search_query)
        #       .select_related("category", "author")
        #       .order_by("-rank"))

        return qs

    def get_context_data(self, **kwargs):
        """
        Template uchun qo'shimcha kontekst: qidiruv so'zi va
        'results' nomi bilan page_obj (template'ni o'zgartirmaslik uchun).
        Shuningdek GET parametrlaridan page ni olib tashlab querystring yaratamiz,
        pagination linklarida boshqa GET paramlarni saqlash uchun qulay.
        """
        context = super().get_context_data(**kwargs)

        # original qidiruv so'zi
        context["query"] = self.request.GET.get("q", "")

        # Templateingiz FBV versiyasida `results` page obyekti sifatida foydalanilgani uchun:
        context["results"] = context.get("page_obj")

        # GET paramlarni saqlab paginationda ishlatamiz (page dan tashqari)
        # params = self.request.GET.copy()
        # if "page" in params:
        #     params.pop("page")
        # context["querystring"] = params.urlencode()  # "" yoki "q=term&other=val"

        params = self.request.GET.copy()
        params.pop("page", None)
        context["querystring"] = params.urlencode()
        
        return context

        

