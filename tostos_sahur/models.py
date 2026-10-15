from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Prefer not to say", "Prefer not to say"),
    ]

    student_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    course = models.CharField(max_length=150)
    year_level = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=30)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.student_id} - {self.last_name}, {self.first_name}"
