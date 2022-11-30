from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
import os
from django.conf import settings
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    image = models.ImageField(upload_to='uploads/',blank=True,null=True)
    thumbnail = models.ImageField(upload_to='uploads/',blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000'+self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000'+self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000'+self.thumbnail.url
            else:
                return ''
    def make_thumbnail(self,image,size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail = File(thumb_io,name=image.name)

        return thumbnail

    def delete(self,*args,**kwargs):
        if self.image:
            os.remove(str(settings.BASE_DIR)+self.image.url)
        if self.thumbnail:
            os.remove(str(settings.BASE_DIR)+self.thumbnail.url)

        super(Product,self).delete(*args,**kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id