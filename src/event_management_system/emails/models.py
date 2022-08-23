from django.db import models

# Create your models here.
class Email(models.Model):
    name = models.CharField(max_length=100)   
    subject = models.CharField(max_length=100)
    answer_to_email = models.EmailField()
    body = models.CharField(max_length=8192) 

    def __str__(self) -> str:
        return self.name