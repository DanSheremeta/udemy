from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return self.name
