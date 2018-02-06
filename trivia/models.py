from django.db import models
from .choices import CategoryType

# Create your models here.


class Answer(models.Model):
    content = models.CharField(default='', blank=False, max_length=150)
    correct = models.BooleanField(default=False)

    question = models.ForeignKey('Question', on_delete=models.CASCADE)


class Question(models.Model):
    content = models.TextField(default='', blank=False, max_length=150)
    category = models.CharField(max_length=20, choices=CategoryType.choices)

    def __str__(self):
        return self.content
