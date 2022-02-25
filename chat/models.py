import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import User
import uuid
import os
class Room(models.Model):
    rid = models.TextField(null=True , blank=True,unique=True)
    users = models.ManyToManyField(User)    
    lastdate = models.DateTimeField(null=True,auto_now=True ,blank=True)
class Message(models.Model):
    mtype = models.CharField(max_length=100)  
    mfile = models.FileField(upload_to='go' , null=True , blank=True)
    content = models.CharField(max_length=5000 , null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room , related_name='messages', verbose_name="rooms",
       on_delete=models.CASCADE)
    okundu = models.BooleanField(default=False, null=True)
    def filetype(self):
        name, extension = os.path.splitext(self.mfile.name)
        if extension in ['.jpg' ,'.png' , '.jpeg']:
            return 'ok'
@receiver(post_save,sender=Room)
def obj_save(sender,instance,created,*args,**kwargs):
    if created:
        uq = uuid.uuid4().hex
        uq += str(instance.id)
        instance.rid = uq
        instance.save()
@receiver(post_save,sender=Message)
def msg_save(sender,instance,created,*args,**kwargs):
    if created:
        instance.room.lastdate= datetime.datetime.now()
        instance.room.save()    