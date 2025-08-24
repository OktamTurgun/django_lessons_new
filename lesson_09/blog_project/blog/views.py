from django.shortcuts import render
from .models import Post

# Create your views here.
def bloglistview(request):
    posts = Post.objects.all()

    context = {
        "posts": posts,
    }
    return render(request, "home.html", context=context)