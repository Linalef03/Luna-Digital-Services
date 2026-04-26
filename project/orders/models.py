from django.db import models
from django.contrib.auth.models import User
from services.models import Service  

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),       
        ('assigned', 'Assigned'),     
        ('in_progress', 'In Progress'), 
        ('completed', 'Completed'),   
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders"
    )

    final_file = models.FileField(upload_to="final_files/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"
