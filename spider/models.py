from django.db import models
import uuid

# Create your models here.
class Post(models.Model):
    STAR = "star"
    STANDARD = "standard"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True)
    content = models.JSONField()
    source = models.CharField(max_length=255)
    is_posted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def mark_as_posted(self):
        self.is_posted = True
        self.save()
