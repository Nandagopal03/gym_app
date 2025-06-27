# gym_app/models.py

from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('client', 'date')  # Prevent duplicate records

    def __str__(self):
        return f"{self.client.username} - {self.date} - {'Present' if self.present else 'Absent'}"



class Fee(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.client.username} - ₹{self.amount} - {'Paid' if self.paid else 'Unpaid'}"

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.png')
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    alt_phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    medical_condition = models.TextField(blank=True)

    def __str__(self):
        return self.full_name