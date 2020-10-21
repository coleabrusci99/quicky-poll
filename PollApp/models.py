from django.db import models
from shortuuidfield import ShortUUIDField

# Create your models here.


class Poll(models.Model):
    topic = models.CharField(max_length=100)
    answers_amount = models.IntegerField()
    url = ShortUUIDField(max_length=10)

    def __str__(self):
        return self.topic


class Answer(models.Model):
    option = models.CharField(max_length=100)
    tally = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.option
