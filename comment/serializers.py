from rest_framework import serializers
from .models import Comment

# Convert model instances to JSON
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("file", "file_name", "title", "file_size", "word_count")