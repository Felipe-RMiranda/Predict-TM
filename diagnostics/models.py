from django.db import models

class Diagnosis(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    img = models.BinaryField()
    probability = models.FloatField()
    status = models.CharField(max_length=50)
    result = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.result} ({self.probability:.2f})"