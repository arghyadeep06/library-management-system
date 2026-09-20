from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_view),
    path('signup/', views.signup_view),
    path('search/', views.search_books),
    path('issue/<int:book_id>/', views.issue_book),
    path('return/<int:issue_id>/', views.return_book),
    path('logout/', views.logout_view, name='logout'),
]