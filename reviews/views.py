from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import AlbumReview
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    reviews = AlbumReview.objects.all()
    return render(request, 'pages/index.html', {'reviews': reviews})

def search_view(request):
    query = request.GET.get('q')
    reviews = []
    if query:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM reviews_albumreview WHERE title LIKE '%{query}%'")
            rows = cursor.fetchall()
            for row in rows:
                reviews.append({'title': row[1], 'content': row[2], 'rating': row[3]})
    return render(request, 'pages/search.html', {'reviews': reviews})

@csrf_exempt
@login_required
def add_review(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = request.POST.get('rating')
        AlbumReview.objects.create(title=title, content=content, rating=rating, author=request.user)
        return redirect('/')
    return render(request, 'pages/add_review.html')

@login_required
def delete_review(request, id):
    review = AlbumReview.objects.get(id=id)
    review.delete()
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('/')
        else:
            return HttpResponse("Wrong username or password")
    return render(request, 'pages/login.html')