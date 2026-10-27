from django.db import models

class PlatformStats(models.Model):
    platform = models.CharField(max_length=30, unique=True)
    handle = models.CharField(max_length=100)
    rating = models.IntegerField(null=True, blank=True)
    max_rating = models.IntegerField(null=True, blank=True)
    solved = models.IntegerField(default=0)
    profile_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform}:{self.handle}"