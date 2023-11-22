from django.db import models

class Comment(models.Model):
    # Simple metadata
    file = models.FileField()
    file_name = models.CharField(max_length=120)
    title = models.CharField(max_length=300)
    file_size = models.PositiveIntegerField()
    word_count = models.PositiveIntegerField()

    def _str_(self):
        return self.title
    