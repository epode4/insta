from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
    }

    return render(request, 'index.html', context)

@login_required
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

@login_required
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

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # 이미 좋아요 버튼을 누른 경우
    if user in post.like_users.all():
        post.like_users.remove(user)
    # if post in user.like_posts.all():
    #     user.like_posts.remove(post)

    # 좋아요 버튼을 아직 안 누른 경우
    else:
        post.like_users.add(user)
        # user.like_posts.add(post)
        


    return redirect('posts:index')


def like_async(request, post_id):
    # context = {
    #     'message': post_id,
    # }

    user = request.user
    post = Post.objects.get(id=post_id)
    
    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count': len(post.like_users.all())
    }

    return JsonResponse(context)

def post_delete(request, post_id):
    post = Post.objects.get(id=post_id)

    username = request.user

    post.delete()

    if 'detail' in request.META.get('HTTP_REFERER'):
        return redirect('accounts:profile', username=username)

    else:
        return redirect('posts:index')


def comment_delete(request, post_id, id):
    comment = Comment.objects.get(id=id)
    
    comment.delete()

    if 'detail' in request.META.get('HTTP_REFERER'):
        return redirect('posts:detail', post_id=post_id)

    else:
        return redirect('posts:index')


def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form,
    }

    return render(request, 'detail.html', context)

@login_required
def detail_comment(request, post_id):
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user= request.user

        post = Post.objects.get(id=post_id)
        comment.post = post

        # comment.post_id = post_id

        comment.save()

        return redirect('posts:detail', post_id=post_id)