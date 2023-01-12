from djongo import models as models

# Create your models here
class Actions(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    dateTime = models.DateTimeField(auto_created=True, auto_now_add=True, blank=True, null=True)
    Code = models.CharField(max_length=1)
    Status = models.CharField(max_length=1)
    Priority = models.CharField(max_length=1)
    Source = models.CharField(max_length=1)

    def __unicode__(self):
        return self._id

class Queue(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    QueueNumber = models.IntegerField(unique=True)
    Action = models.OneToOneField(Actions, on_delete= models.CASCADE, related_name='Action')

    def __unicode__(self):
        return self._id

    objects = models.DjongoManager()