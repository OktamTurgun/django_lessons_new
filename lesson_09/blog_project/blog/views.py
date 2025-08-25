# from django.http import Http404
# from django.shortcuts import render, get_object_or_404
# from .models import Post

# # Create your views here.
# def bloglistview(request):
#     posts = Post.objects.all()

#     context = {
#         "posts": posts,
#     }
#     return render(request, "home.html", context=context)

# def blogdetailview(request, id):
#     post = get_object_or_404(Post, id=id)
#     context = {
#         "post": post,
#     }

#     return render(request, "post_detail.html", context=context)

from .models import Post
from django.views.generic import ListView, DetailView


class BlogListView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    
    