from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'Todo.views.task_page', name='home'),
	url(r'^tasks/$', 'Todo.views.tasks', name='tasks_json'),
	url(r'^create','Todo.views.create_task', name='add_task'),
	url(r'^(?P<tid>\d+)/edit','Todo.views.edit_task', name="edit_task"),
	url(r'^(?P<tid>\d+)/assign','Todo.views.assign_user', name="assign_user"),
	url(r'^(?P<aid>\d+)/delassign','Todo.views.delete_assign_user', name="delete_assign_user"),
	url(r'^ndelete/$', 'Todo.views.ndelete',name="multiple_delete"),
	url(r'^(?P<tid>\d+)/$','Todo.views.task_detail_page', name="task"),
	url(r'^(?P<tid>\d+)/data','Todo.views.task_details', name="task_data"),

	url(r'^comment/add','Todo.views.add_comment', name="add_comment"),
	url(r'^comment/(?P<cid>\d+)/edit','Todo.views.edit_comment', name="edit_comment"),
	url(r'^comment/(?P<cid>\d+)/delete','Todo.views.delete_comment', name="delete_comment"),

)