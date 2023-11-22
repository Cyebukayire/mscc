from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_name', 'title', 'file_size', 'word_count')

# Register model
admin.site.register(Comment, CommentAdmin)