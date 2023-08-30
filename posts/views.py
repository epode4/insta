from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id')

    context = {
        'posts': posts
    }

    return render(request, 'index.html', context)

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')

    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'form.html', context)