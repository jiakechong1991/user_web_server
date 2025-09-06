from django.db import models

# Create your models here.

class TQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class TChoice(models.Model):
    question = models.ForeignKey(TQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)