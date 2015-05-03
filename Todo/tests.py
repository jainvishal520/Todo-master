import json
import datetime
from django.core import serializers
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser 
from Todo.models import Task,Comment, Assigned
from Todo.views import tasks, task_page, task_details


class TaskUnitTest(TestCase):
	'''Unit test for Task model'''

	def setUp(self):
		self.user = User.objects.create_user(username='kantesh', email='kanteshraj@gmail.com', password='top_secret')
		Task.objects.create(user=self.user,name='testing',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')
	
	def test_task_attribute(self):
		task = Task.objects.get(user=self.user)
		self.assertEqual(task.name, 'testing')
		self.assertEqual(task.description, 'testing this task')
		self.assertEqual(task.priority, '1')
		self.assertEqual(task.status, '1')
		self.assertEqual(str(task.due_date.date()), '2014-06-06')
		self.assertEqual(str(task.due_date.time()), '00:50:00') # DateTime is saved in UTC Format
		self.assertNotEqual(str(task.due_date.time()), '06:20:00') # DateTime is saved in UTC Format



class CommentUnitTest(TestCase):
	'''Unit test for Comment Model'''

	def setUp(self):
		self.user = User.objects.create_user(username='kantesh', email='kanteshraj@gmail.com', password='top_secret')
		self.task1 = Task.objects.create(user=self.user,name='testing',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')
		self.task2 = Task.objects.create(user=self.user,name='testing',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')
		Comment.objects.create(task=self.task1,description="test comment 1",user=self.user)
		Comment.objects.create(task=self.task1,description="test comment 2",user=self.user)
		Comment.objects.create(task=self.task2,description="test comment 3",user=self.user)

	def test_comments(self):
		comments_task1 = Comment.objects.filter(task=self.task1)
		comments_task2 = Comment.objects.filter(task=self.task2)
		comments_user = Comment.objects.filter(user=self.user)
		comment = Comment.objects.get(task=self.task2)
		self.assertEqual(comments_task1.count(), 2)
		self.assertEqual(comments_task2.count(), 1)
		self.assertEqual(comments_user.count(), 3)
		self.assertNotEqual(comment.description, "test comment 2")
		self.assertEqual(comment.description, "test comment 3")




class AssignedUnitTest(TestCase):
	'''Unit test for Assigned model'''

	def setUp(self):
		self.user = User.objects.create_user(username='kantesh', email='kanteshraj@gmail.com', password='top_secret')
		self.user1 = User.objects.create_user(username='kantesh1', email='kanteshraj1@gmail.com', password='top_secret')
		self.task = Task.objects.create(user=self.user,name='testing',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')
		Assigned.objects.create(task=self.task,to=self.user1)

	def test_task_assignment(self):
		user_task = Task.objects.filter(user=self.user)
		user1_task = Task.objects.filter(user=self.user1)
		user_assigned_task = Assigned.objects.filter(to=self.user)
		user1_assigned_task = Assigned.objects.filter(to=self.user1)
		assigned_task = user1_assigned_task[0].task
		self.assertEqual(user_task.count(), 1)
		self.assertEqual(user1_task.count(), 0)
		self.assertEqual(user_assigned_task.count(), 0)
		self.assertEqual(user1_assigned_task.count(), 1)
		self.assertEqual(assigned_task.name, 'testing')




# Integration Test
class PageViewPermissionTest(TestCase):
	'''Only Logged in user can view tasks page'''
	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='kantesh', email='kanteshraj@gmail.com', password='top_secret')

	def test_for_logged_in_user(self):
		request = self.factory.get('/todo/')
		request.user = self.user
		response = task_page(request)
		self.assertEqual(response.status_code, 200)

	def test_for_AnonymousUser(self):	
		request = self.factory.get('/todo/')
		request.user = AnonymousUser()
		request.session = {}
		response = task_page(request)
		self.assertNotEqual(response.status_code, 200)
		self.assertEqual(response.status_code, 302)



class JsonTaskApiTest(TestCase):
	'''Test Json Api for specific Task i.e, /todo/:id/tasks'''

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='kantesh', email='kanteshraj@gmail.com', password='top_secret')
		self.task = Task.objects.create(user=self.user,name='testing',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')
		self.comment = Comment.objects.create(task=self.task,description="test comment 1",user=self.user)

	def task_url(self):
		return '/todo/'+str(self.task.id)+'/data'

	def test_response(self):
		url = self.task_url()
		request = self.factory.get(url)
		request.user = self.user
		response = task_details(request,self.task.id)
		self.assertEqual(response.status_code, 200)
		json_string = response.content
		json_obj = json.loads(json_string)
		self.assertEqual(json_obj["task"]["name"], self.task.name)
		self.assertEqual(json_obj["task"]["description"], self.task.description)
		self.assertEqual(json_obj["task"]["priority"], self.task.priority)
		self.assertEqual(json_obj["task"]["status"], self.task.status)
		self.assertEqual(json_obj["task"]["user"], self.user.username)
		self.assertEqual(len(json_obj["comments"]), 1)
		self.assertEqual(json_obj["comments"][0]["description"], self.comment.description)
		self.assertEqual(json_obj["comments"][0]["user"], self.user.username)
		self.assertEqual(len(json_obj["assign_user"]), 0)



class JsonTasksApiTest(TestCase):
	'''Test Json Api for Tasks'''

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='kantesh', email='kanteshraj@gmail.com', password='top_secret')
		self.task = Task.objects.create(user=self.user,name='testing',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')
		Comment.objects.create(task=self.task,description="test comment 1",user=self.user)
		Comment.objects.create(task=self.task,description="test comment 1",user=self.user)
		self.task1 = Task.objects.create(user=self.user,name='testing1',description='testing this task',priority='1',status='1',due_date='2014-06-06 06:20:00')

	def test_response(self):
		request = self.factory.get('/todo/tasks')
		request.user = self.user
		response = tasks(request)
		self.assertEqual(response.status_code, 200)
		json_string = response.content
		json_obj = json.loads(json_string)
		self.assertEqual(len(json_obj), 2)
		self.assertEqual(json_obj[0]["name"], self.task.name)
		self.assertEqual(json_obj[0]["count"], 2)
		self.assertEqual(json_obj[0]["user"], "kantesh")
		self.assertEqual(json_obj[1]["name"], self.task1.name)
		self.assertEqual(json_obj[1]["count"], 0)
		self.assertEqual(json_obj[1]["user"], "kantesh")


