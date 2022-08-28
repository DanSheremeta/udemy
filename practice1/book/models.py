from django.db import models
from author.models import Author


class Genre(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {self.id}


class Language(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return {self.id}


class Book(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    date_of_publication = models.DateField()
    date_of_writing = models.DateField()

    def __str__(self):
        return f'{self.name}, written by {self.author}'
