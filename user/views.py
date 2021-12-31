from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import User, Bill, Device 
from tool.models import Tool
import uuid
from datetime import datetime, timedelta

def home(request):
	return HttpResponse("home")

def info(request, username):
	if request.method == "GET":
		username = request.GET.get("username")
		password = request.GET.get("password")
	if username is None or password is None:
		return JsonResponse({
			"status":"fail",
			"username":username
			})
	user = User.objects.filter(username=username, password=password)
	if not user:
		return JsonResponse({
			"status":"fail",
			"username":username
			})
	user = user[0]
	return JsonResponse({
		"status":"success",
		"username":username, 
		"money":user.credit, 
		"user_id":user.user_id, 
		"last_use":user.last_use
		})



def refund(request):
	if request.method == "GET":
		bill_id = request.GET.get("bill_id")
		if bill_id is None:
			return JsonResponse({
				"username":username,
				 "status":"fail", 
				 "bill_id":bill_id
				 })
		bill = List(Bill.objects.filter(bill_id=bill_id))
		if bill is None:
			return JsonResponse({
				"status":"fail",
				"username":username,
				"bill_id":bill_id
				})
		bill = bill[0]
		expire = datetime.now().timestamp() - bill.date.timestamp()
		if expire > 600:
			return JsonResponse({
				"status":"fail",
				"username":username, 
				"bill_id":bill_id
				})
		else:
			user = User.objects.filter(username=username, password= password)
			if not user:
				return JsonResponse({
					"username":username,
					"status":"success",
					"bill_id":bill_id
					})
			user = user[0]
			user.credit += bill.payment
			user.save()
			return JsonResponse({
				"status":"fail",
				"username":username,
				"bill_id":bill_id
				})
def device(request):
	if request.method == "GET":
		device_id = request.GET.get("device_id")
		tool_name = request.GET.get("tool")
		if not device_id or not tool_name:
			return JsonResponse({
				"status":"fail", 
				"device_id":device_id,
				"tool":tool_name
				})
		x = List(Device.objects.filter(device_id=device_id, tool_name=tool_name))
		if not x:
			return JsonResponse({
				"status":"fail", 
				"device_id":device_id,
				"tool":tool_name
			})
		else:
			return JsonResponse({
				"status":"success",
				"device_id":device_id,
				"tool":tool_name
				})


def pay(request):	
	if request.method == "GET":
		username = request.GET.get("username")
		password = request.GET.get("password")
		if username is None or password is None:
			return JsonResponse({
				"username":username,
				"status":"fail"
				})
		tool = request.GET.get("tool")
		if tool is None: 
			return JsonResponse({
				"username":username, 
				"status":"fail"
				})

		user = list(User.objects.filter(username=username, password=password))
		if not user:
			return JsonResponse({
				"username":username,
				"tool":tool,
				"status":"fail"
				})
		t = list(Tool.objects.filter(name=tool))
		if not t:
			return JsonResponse({
				"username":username,
				"tool":tool,
				"status":"fail"
				}) 
		t = t[0]
		user = user[0]
		if user.credit < t.cost:
			return JsonResponse({
				"username":username,
				"tool":tool,
				"cost":t.cost,
				"money":user.credit
				})
		user.credit -= t.cost
		user.save()
		bill = Bill(bill_id=uuid.uuid4().hex[:30].upper(),
			user_id=user.user_id,
			payment=t.cost)
		bill.save()
		return JsonResponse({
			"status" : "success",
		 	"tool":tool, 
		 	"cost":t.cost, 
		 	"money":user.credit, 
		 	"bill_id":bill.bill_id
		 	})
		
	return JsonResponse({"status":401}) 