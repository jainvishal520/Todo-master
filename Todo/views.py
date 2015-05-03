import json
import pytz
import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.core import serializers
from Todo.models import Task
from Todo.models import Comment
from Todo.models import Assigned


@login_required(login_url=reverse('user:login'))
def task_page(request):
	return render(request,'Todo/tasks.html')

@login_required(login_url=reverse('user:login'))
def tasks(request):
	task_array = self_owned_task(request.user)
	task_array = task_array + assigned_task(request.user)
	return HttpResponse(json.dumps(task_array,cls=DjangoJSONEncoder), content_type="application/json")

@login_required(login_url=reverse('user:login'))
def create_task(request):
  if request.method=='POST': 
  	due_date = string_to_datetime(request.POST.get('date_post'))
   	Task.objects.create(user=request.user,name=request.POST.get('name'),description=request.POST.get('description'),priority=request.POST.get ('priority'),due_date=due_date)
   	return HttpResponseRedirect(reverse('todo:home')) 

@login_required(login_url=reverse('user:login'))
def ndelete(request):
	if request.method == "GET":
		return render(request,'Todo/delete.html')
	else:
		tasks_id = request.POST.getlist('tasks_id')
		for i in tasks_id:
			task = Task.objects.get(id=str(i))
			if task.user == request.user:
				task.delete()
		return HttpResponseRedirect(reverse('todo:home'))


@login_required(login_url=reverse('user:login'))
def task_detail_page(request,tid):
	try:
		task = Task.objects.get(id=tid)
	except (ValueError, ObjectDoesNotExist):
		messages.add_message(request, messages.INFO, 'Incorrect Task Id')
		return HttpResponseRedirect(reverse('todo:home'))
	else:
		if check_task_permission(request,task):
			return render(request,'Todo/edit.html',{'tid' : tid})
		else:
			messages.add_message(request, messages.INFO, 'Incorrect Permission')	
			return HttpResponseRedirect(reverse('todo:home'))



@login_required(login_url=reverse('user:login'))
def task_details(request,tid):
	task = Task.objects.get(id=tid)
	if check_task_permission(request,task):
		resp = {}
		resp['task'] = task_dictionary(task)
		resp['comments'] = get_comment(task)
		resp['assign_user'] = get_assigned_user(task)
		return HttpResponse(json.dumps(resp,cls=DjangoJSONEncoder), content_type="application/json")
	else:
		messages.add_message(request, messages.INFO, 'Incorrect Permission')
		return HttpResponseRedirect(reverse('todo:home'))

@login_required(login_url=reverse('user:login'))
def edit_task(request,tid):
	if request.method == "POST":
		task = Task.objects.get(id=tid)
		if check_task_permission(request,task):
			# print request.POST
			task.priority = request.POST.get('priority')
			task.status = request.POST.get('status')
			if request.POST.get('due_date').find('-') < 0:
				task.due_date = string_to_datetime(request.POST.get('due_date'))
			task.save()
			return HttpResponseRedirect(reverse('todo:home')+str(tid)+'/')
		else:
			messages.add_message(request, messages.INFO, 'Incorrect Permission')
			return HttpResponseRedirect(reverse('todo:home'))


@login_required(login_url=reverse('user:login'))
def assign_user(request,tid):
	if request.method == "POST":
		task = Task.objects.get(id=tid)
		if check_task_permission(request,task):
			status,user = get_user(request.POST.get('user_name'))
			if status:
				if not(is_already_assigned(user,task)):
					Assigned.objects.create(task=task,to=user)
			else:
				messages.add_message(request, messages.INFO, 'Username doesnot exists. Please assign task to different user')
			return HttpResponseRedirect(reverse('todo:home')+str(tid)+'/')
		else:
			messages.add_message(request, messages.INFO, 'Incorrect Permission')
			return HttpResponseRedirect(reverse('todo:home'))

@login_required(login_url=reverse('user:login'))
def delete_assign_user(request,aid):
	if request.method == "GET":
		assigned_task = Assigned.objects.get(id=aid)
		tid = assigned_task.task.id
		assigned_task.delete()
		return HttpResponseRedirect(reverse('todo:home')+str(tid)+'/')
	else:
		messages.add_message(request, messages.INFO, 'Incorrect Permission')
		return HttpResponseRedirect(reverse('todo:home'))


@login_required(login_url=reverse('user:login'))
def add_comment(request):
	tid = request.POST.get('task_id')
	task = Task.objects.get(id=tid)
	if task.user == request.user:
		message = request.POST.get('message')
		Comment.objects.create(user=request.user,task=task,description=message)
		return HttpResponseRedirect(reverse('todo:home')+tid+'/')
	else:
		messages.add_message(request, messages.INFO, 'Incorrect Permission')
		return HttpResponseRedirect(reverse('todo:home'))	

@login_required(login_url=reverse('user:login'))
def add_comment(request):
	tid = request.POST.get('task_id')
	task = Task.objects.get(id=tid)
	message = request.POST.get('message')
	Comment.objects.create(user=request.user,task=task,description=message)
	return HttpResponseRedirect(reverse('todo:home')+tid+'/')


@login_required(login_url=reverse('user:login'))
def delete_comment(request,cid):
	comment = Comment.objects.get(id=cid)
	task = comment.task
	if comment.user == request.user or task.user == request.user:
		comment.delete()
		tid = task.id
		return HttpResponseRedirect(reverse('todo:home')+str(tid)+'/')
	else:
		messages.add_message(request, messages.INFO, 'Incorrect Permission')
		return HttpResponseRedirect(reverse('todo:home'))

@login_required(login_url=reverse('user:login'))
def edit_comment(request,cid):
	if request.method == "GET":
		comment = Comment.objects.get(id=cid)
		if comment.user == request.user:
			desc = comment.description
			return render(request,'Todo/edit_comment.html',{'id':cid,'desc':desc})
		return HttpResponseRedirect(reverse('todo:home'))
	else:
		comment = Comment.objects.get(id=cid)
		tid = comment.task.id
		comment.description = request.POST.get('message')
		comment.save()
		return HttpResponseRedirect(reverse('todo:home')+str(tid)+'/')


# Helper Function
# ==================

def check_task_permission(request,task):
	if task.user == request.user:
		return True
	assigned_tasks = Assigned.objects.filter(task=task)
	for i in assigned_tasks:
		if i.to == request.user:
			return True
	return False

def task_dictionary(task):
	temp = {}
   	temp["id"] = task.id
   	temp["user"] = task.user.username
   	temp["name"] = task.name
   	temp["status"] = task.status
   	temp["due_date"] = local_date_time(task.due_date) 
   	temp["priority"] = task.priority
   	temp["description"] = task.description
   	temp["timestamp"]= local_date_time(task.timestamp)
   	temp["count"]= comment_count(task)
   	return temp

def self_owned_task(user):
	tasks = Task.objects.filter(user=user)
	task_array = []
  	for i in tasks:
  		task_dic = task_dictionary(i)
   		task_array.append(task_dic)
  	return task_array

def comment_count(task):
	comments = Comment.objects.filter(task=task)
	return comments.count()

def assigned_task(user):
	task_array = []
	for i in Assigned.objects.filter(to=user):
		task = i.task
		if i.to == task.user:
			continue
   		task_dic = task_dictionary(task)
   		task_array.append(task_dic)
   	return task_array

def get_user(username):
	try:
		user = User.objects.get(username=username)
	except (ValueError, ObjectDoesNotExist):
		return False,''
	else:
		return True,user

def is_already_assigned(user,task):
	assigned = Assigned.objects.filter(task=task)
	for i in assigned:
		if i.to == user:
			return True
	return False

def local_date_time(date_time):
	date_time = date_time.replace(tzinfo=pytz.utc) + datetime.timedelta(hours=5, minutes=30)
	date_time = date_time.strftime("%Y-%m-%d %I:%M %p")
	return date_time

def string_to_datetime(string):
	date_time = datetime.datetime.strptime(string,'%m/%d/%Y %I:%M %p')
	ist = pytz.timezone('Asia/Kolkata')
	date_time = ist.localize(date_time)
	return date_time


def get_comment(task):
	comments = []
	for i in Comment.objects.filter(task=task):
		comment = {}
		comment["id"] = i.id
		comment["description"] = i.description
		comment["timestamp"] = local_date_time(i.timestamp)
		comment["user"] = str(i.user)
		comments.append(comment)
	return comments

def get_assigned_user(task):
	assign_user = []
	for i in Assigned.objects.filter(task=task):
		temp={}
   		temp["user"]= str(i.to)
   		temp["id"]=i.id	
   		assign_user.append(temp)
	return assign_user