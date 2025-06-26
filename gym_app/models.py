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
