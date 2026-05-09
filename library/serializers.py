from rest_framework import serializers

from .models import Book, BookIssue
from profiles.models import StudentProfile


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book

        fields = '__all__'


class BookIssueSerializer(serializers.ModelSerializer):

    student_id = serializers.IntegerField()
    book_id = serializers.IntegerField()

    class Meta:
        model = BookIssue

        fields = [
            'student_id',
            'book_id'
        ]

    def create(self, validated_data):

        student_id = validated_data.pop('student_id')
        book_id = validated_data.pop('book_id')

        student = StudentProfile.objects.get(id=student_id)

        book = Book.objects.get(id=book_id)

        if book.available_copies <= 0:
            raise serializers.ValidationError(
                "No copies available"
            )

        book.available_copies -= 1
        book.save()

        issue = BookIssue.objects.create(
            student=student,
            book=book,
            issued_by=self.context['request'].user
        )

        return issue