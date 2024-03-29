from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=150)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.FileField(upload_to="blog_images/", blank=False)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
        
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def pending_comments(self):
        approved_comment_count = len(self.comments.filter(approved_comment=True)) 
        total_comment_count = len(self.comments.all())
        return total_comment_count - approved_comment_count
    
            # Provides the first section of the text for preview  
    def incipit_long(self):
        return self.text[0:299]
   
    def incipit_short(self):
        return self.text[0:99]
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text