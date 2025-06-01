from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
import sys

from blog.forms import CommentForm, PasswordChangeForm, PostForm, ProfileForm
from blog.models import Category, Comment, Post
from blogicum.settings import POSTS_PER_PAGE


def index(request):
    posts = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    posts = category.posts.filter(
        is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/category.html', {'category': category, 'page_obj': page_obj})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = profile.posts.all()
    if request.user != profile:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
    posts = posts.annotate(comment_count=Count(
        'comments')).order_by('-pub_date')
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'blog/profile.html', {'profile': profile, 'page_obj': page_obj})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password1'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PasswordChangeForm()
    return render(request, 'blog/password_change_form.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        if not post.is_published or not post.category.is_published or post.pub_date > timezone.now():
            return render(request, 'pages/404.html', status=404)
    form = CommentForm()
    comments = post.comments.all().order_by('created_at')
    print(f"post_detail: User={request.user.username if request.user.is_authenticated else 'Anonymous'}, "
          f"UserID={request.user.id if request.user.is_authenticated else 'None'}, "
          f"PostID={post.id}, "
          f"Comments={[(c.id, c.author.username, c.author.id) for c in comments]}", file=sys.stderr)  # Отладка
    return render(request, 'blog/detail.html', {
        'post': post,
        'form': form,
        'comments': comments
    })


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/create.html', {'form': form, 'is_edit': True})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return HttpResponseForbidden('Нельзя удалять чужие посты.')
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'post': post, 'is_delete': True})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                print("add_comment: User not authenticated",
                      file=sys.stderr)  # Отладка
                return redirect('blog:post_detail', post_id=post_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            print(f"add_comment: Created comment by {comment.author.username} (ID={comment.author.id}) "
                  f"for post {post_id}, CommentID={comment.id}, PostID={post.id}", file=sys.stderr)  # Отладка
            return redirect('blog:post_detail', post_id=post_id)
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden('Нельзя редактировать чужие комментарии.')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html', {'form': form, 'comment': comment, 'is_edit': True})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Требуется авторизация.')
    if comment.author != request.user:
        return HttpResponseForbidden('Нельзя удалять чужие комментарии.')
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)
    return render(request, 'blog/comment.html', {'comment': comment, 'is_delete': True})
