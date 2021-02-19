from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)

    def was_published_recently(self):
        return self.pub_date >= timezone.now()

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('polls:index')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def get_absolute_url(self):
        return reverse('polls:detail', args=str(self.question.pk))