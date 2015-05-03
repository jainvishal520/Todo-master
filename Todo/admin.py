from django.contrib import admin
from Todo.models import Task
from Todo.models import Comment
from Todo.models import Assigned

admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Assigned)

