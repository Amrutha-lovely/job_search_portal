from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    salary = models.CharField(max_length=100)
    skills = models.TextField()

    def __str__(self):
        return self.title

