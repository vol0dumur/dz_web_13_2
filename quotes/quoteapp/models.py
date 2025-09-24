from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=75, null=False, unique=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        self.name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Tags"
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]


class Quote(models.Model):
    quote_text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.quote_text}"
    
    class Meta:
        verbose_name_plural = "Quotes"


class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    born = models.DateField(null=False)
    # died = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Authors"