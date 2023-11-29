from rest_framework import serializers
from .models import Comment
from .metadata import Metadata

# Convert model instances to JSON
class CommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return super().to_representation(instance)  # Use the default representation

    def create(self, validated_data):
        metadata = Metadata()

        # Extract metadata before creating the Comment object
        metadata = metadata.extract_all(validated_data)

        # Add metadata to validated_data
        validated_data.update(metadata)

        # Create the Comment object
        return super().create(validated_data)

    class Meta:
        model = Comment
        fields = ["file", "file_name", "title", "file_size", "word_count"] # Display all fields by default
