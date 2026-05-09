from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Book, BookIssue
from .serializers import (
    BookSerializer,
    BookIssueSerializer
)

from .permissions import IsLibrarian
from drf_spectacular.utils import extend_schema

# ADD BOOK
class AddBookView(APIView):

    permission_classes = [IsAuthenticated, IsLibrarian]

    @extend_schema(
    responses={201: "Created Successfully"}
)
    def post(self, request):

        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# LIST BOOKS
class BookListView(APIView):

    permission_classes = [IsAuthenticated]
    @extend_schema(
    responses={200: list}
)
    def get(self, request):

        books = Book.objects.all()

        serializer = BookSerializer(books, many=True)

        return Response(serializer.data)


# UPDATE BOOK
class UpdateBookView(APIView):

    permission_classes = [IsAuthenticated, IsLibrarian]
    
    @extend_schema(
    responses={200: "Updated Successfully"}
)
    def put(self, request, pk):

        try:
            book = Book.objects.get(id=pk)

        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=404
            )

        serializer = BookSerializer(
            book,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


# ISSUE BOOK
class IssueBookView(APIView):

    permission_classes = [IsAuthenticated, IsLibrarian]

    @extend_schema(
    responses={201: "Created Successfully"}
)
    def post(self, request):

        serializer = BookIssueSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Book issued successfully"}
            )

        return Response(serializer.errors, status=400)


# RETURN BOOK
class ReturnBookView(APIView):

    permission_classes = [IsAuthenticated, IsLibrarian]
    @extend_schema(
    responses={201: "Created Successfully"}
)
    def post(self, request):

        issue_id = request.data.get('issue_id')

        try:
            issue = BookIssue.objects.get(id=issue_id)

        except BookIssue.DoesNotExist:
            return Response(
                {"error": "Issue record not found"},
                status=404
            )

        if issue.is_returned:
            return Response(
                {"error": "Book already returned"},
                status=400
            )

        issue.is_returned = True
        issue.return_date = date.today()
        issue.save()

        book = issue.book
        book.available_copies += 1
        book.save()

        return Response(
            {"message": "Book returned successfully"}
        )


# STUDENT BORROWED BOOKS
class StudentBorrowedBooksView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
    responses={200: list}
)
    def get(self, request):

        if request.user.role != "student":
            return Response(
                {"error": "Only students allowed"},
                status=403
            )

        student_profile = request.user.student_profile

        books = BookIssue.objects.filter(
            student=student_profile,
            is_returned=False
        )

        data = []

        for item in books:
            data.append({
                "book": item.book.title,
                "author": item.book.author,
                "issue_date": item.issue_date
            })

        return Response(data)