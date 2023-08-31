from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm

# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
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


def comment_create(request, post_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user= request.user

        post = Post.objects.get(id=post_id)
        comment.post = post

        # comment.post_id = post_id

        comment.save()

        return redirect('posts:index')
