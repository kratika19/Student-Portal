from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# sagar810
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'All Notes'

    def __str__(self):
        return self.title
