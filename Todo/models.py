from django.db import models
from datetime import datetime   
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255,null=True)
    description = models.TextField()
    priority = models.CharField(max_length=1,choices=(('1','Low'),('2','Medium'),('3','High')),default="1")
    status = models.CharField(max_length=1,choices=(('0','Pending'),('1','Done')),default="0")
    due_date = models.DateTimeField(max_length=255,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
   
class Comment(models.Model):
    task = models.ForeignKey(Task)
    description = models.TextField()
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.description
    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Assigned(models.Model):
    task = models.ForeignKey(Task)
    to = models.ForeignKey(User)
    def __str__(self):
        return str(self.task)
    class Meta:
        db_table = 'assigned_task'
        verbose_name = 'Assigned task'
        verbose_name_plural = 'Assigned tasks'