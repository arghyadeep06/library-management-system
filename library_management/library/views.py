from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Book
from .models import Issue
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.contrib.auth import logout
from django.http import JsonResponse
def home(request):
    books = Book.objects.all()

    if request.user.is_authenticated:
        issued_books = Issue.objects.filter(
            user=request.user,
            return_date__isnull=True
        )
    else:
        issued_books = []   # VERY IMPORTANT

    return render(request, 'home.html', {
        'books': books,
        'issued_books': issued_books
    })
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # go to home
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        return redirect('/login')

    return render(request, 'signup.html')

def search_books(request):
    query = request.GET.get('q')
    books = Book.objects.filter(title__icontains=query) if query else []
    
    return render(request, 'home.html', {'books': books})
def issue_book(request, book_id):
    book = Book.objects.get(id=book_id)

    issued_count = Issue.objects.filter(user=request.user, return_date__isnull=True).count()

    if issued_count >= 3:
        return HttpResponse("You can only issue 3 books")

    if book.available_copies <= 0:
        return HttpResponse("No copies available")

    due_date = timezone.now().date() + timedelta(days=7)

    Issue.objects.create(
        user=request.user,
        book=book,
        due_date=due_date
    )

    book.available_copies -= 1
    book.save()

    return redirect('/')
from django.http import JsonResponse
from django.utils import timezone

def return_book(request, issue_id):
    issue = Issue.objects.get(id=issue_id)

    issue.return_date = timezone.now()
    issue.book.available_copies += 1
    issue.book.save()
    issue.save()

    return JsonResponse({"message": "Book returned successfully ✅"})

def logout_view(request):
    logout(request)
    return redirect('/')

# Create your views here.
