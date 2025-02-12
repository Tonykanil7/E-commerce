from django.db import models

# Create your models here.

class Menu(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name=models.CharField(max_length=20)
    price=models.IntegerField()
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE,related_name='items')
    is_vegetarian=models.BooleanField(default=True)

    def __str__(self):
        return self.name