from django.db import models

# Create your models here.


from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    image = models.ImageField(upload_to='media/category',blank=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()
    image = models.ImageField(upload_to='media/products',blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    available=models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name