from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userprofile')
    bio = models.TextField(blank=True)
    img = models.ImageField(upload_to='profilepictures')
    address = models.TextField(blank=True)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username
class Category(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title
class Ad(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=True)
    Description = models.TextField(blank=True)
    Price = models.IntegerField(null=True)
    image = models.ImageField(null=True,upload_to='adimage')
    contact = models.IntegerField(null=True)
    Email = models.EmailField(blank=True)
class Adimage(models.Model):
    ad = models.ForeignKey(Ad,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='ad_images',blank=True)
    def __str__(self):
        return f'image for {self.ad.title}'
class Contact(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sentmessages',null=True)
    reciever = models.ForeignKey(User,on_delete=models.CASCADE,related_name='recievemessages',null=True)
    message = models.TextField()
    ad = models.ForeignKey(Ad,on_delete=models.CASCADE,null=True,related_name='interested_ad')
    def __str__(self):
        return self.sender.username
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sent_messages")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_message')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']