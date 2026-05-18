from django.urls import path

from .views import (
    AddBookView,
    BookListView,
    UpdateBookView,
    IssueBookView,
    ReturnBookView,
    StudentBorrowedBooksView,
    BookDetailView
)

urlpatterns = [

    path(
        'books/add/',
        AddBookView.as_view()
    ),

    path(
        'books/',
        BookListView.as_view()
    ),
    
    path(
        'books/<int:pk>/',
        BookDetailView.as_view()
        
    ),


    
    path('books/<int:pk>/update/', UpdateBookView.as_view()),

    path(
        'books/issue/',
        IssueBookView.as_view()
    ),

    path(
        'books/return/',
        ReturnBookView.as_view()
    ),

    path(
        'student/books/',
        StudentBorrowedBooksView.as_view()  # sees own borrowed books
    ),
    
    
]


