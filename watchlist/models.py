from django.db import models

# Create your models here.
class Watchlist(models.Model):
    profile_id = models.IntegerField(default=1)
    content_id = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=6)
    date = models.CharField(max_length=32)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
