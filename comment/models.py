from django.db import models

class Comment(models.Model):
    # Simple metadata
    id = models.CharField(primary_key=True, max_length=19, blank=True)
    file = models.FileField(upload_to='uploads/')
    file_name = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=300, blank=True)
    file_size = models.BigIntegerField(blank=True, null=True)
    word_count = models.BigIntegerField(blank=True, null=True)

    def _str_(self):
        return self.title
    