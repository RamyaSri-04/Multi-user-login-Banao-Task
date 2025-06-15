from django.db import models

class Patient(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"Patient - {self.username}"

class Doctor(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"Doctor - {self.username}"