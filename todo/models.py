from django.db import models
from django.urls import reverse

from accounts.models import CustomUser

class TodoItem(models.Model):
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    def get_absolute_url(self):
        return reverse('todoitem_detail', arts=[str(self.id)])