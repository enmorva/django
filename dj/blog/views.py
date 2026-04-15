from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import News, Comment
from .forms import RegisterForm, CommentForm


def home(request):
    latest_news = News.objects.all()[:3]  # последние 3 новости
    return render(request, 'blog/home.html', {'latest_news': latest_news})


def contact(request):
    return render(request, 'blog/contact.html')


def news_list(request):
    news_query = News.objects.all()

    # Поиск по названию
    search_query = request.GET.get('search', '')
    if search_query:
        news_query = news_query.filter(title__icontains=search_query)

    # Сортировка (по умолчанию новые сначала)
    sort = request.GET.get('sort', 'desc')
    if sort == 'asc':
        news_query = news_query.order_by('published_date')
    else:
        news_query = news_query.order_by('-published_date')

    return render(request, 'blog/news_list.html', {
        'news_list': news_query,
        'search_query': search_query,
        'current_sort': sort
    })


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            return redirect('news_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'blog/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'blog/login.html', {'error': 'Неверные данные'})
    return render(request, 'blog/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')