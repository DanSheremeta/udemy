from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    birth_date = models.DateField()
    age = models.IntegerField(default=None)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} {self.surname}'
