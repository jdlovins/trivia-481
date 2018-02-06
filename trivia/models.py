from django.db import models

# Create your models here.


class Answer(models.Model):
    main = models.CharField(default='', blank=False, max_length=150)


class Question(models.Model):
    content = models.CharField(default='', blank=False, max_length=150)
    ans = models.ForeignKey(Answer, on_delete=models.CASCADE)
