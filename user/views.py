from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import User, Bill
from tool.models import Tool
import uuid
from datetime import datetime, timedelta

def home(request):
	return HttpResponse("home")

def pay(request):	
	if request.method == "GET":
		username = request.GET.get("username")
		password = request.GET.get("password")
		action   = request.GET.get("action")
		if username is None or password is None or action is None:
			return JsonResponse({"username":username, "action":action, "status":"fail"})
		if action=="user tool":		
			tool = request.GET.get("tool")
			if tool is None: 
				return JsonResponse({"username":username, "action":action, "status":"fail"})
			user = list(User.objects.filter(username=username, password=password))
			if not user:
				return JsonResponse({"username":username, "action":action, "tool":tool, "status":"fail"})
			t = list(Tool.objects.filter(name=tool))
			if not t:
				return JsonResponse({"username":username, "action":action, "tool":tool, "status":"fail"}) 
			t = t[0]
			user = user[0]
			if user.credit < t.cost:
				return JsonResponse({"username":username, "action":action, "tool":tool, "cost":t.cost, "money":user.credit})
			user.credit -= t.cost
			user.save()
			bill = Bill(bill_id=uuid.uuid4().hex[:30].upper(),
				user_id=user.user_id,
				payment=t.cost)
			bill.save()
			return JsonResponse({"status" : "success", "action":action, "tool":tool, "cost":t.cost, "money":user.credit, "bill id":bill.bill_id})
		elif action=="refund":
			bill_id = request.GET.get("bill id")
			if bill_id is None:
				return JsonResponse({"username":username, "action":action, "status":"fail"})
			bill = Bill.objects.filter(bill_id=bill_id)
			if bill is None:
				return JsonResponse({"status":"fail", "action":action, "username":username, "bill id":bill_id})
			bill = bill[0]
			expire = datetime.now().timestamp() - bill.date.timestamp()
			if expire > 600:
				return JsonResponse({"status":"fail", "action":action, "username":username, "bill id":bill_id})
			else:
				user = User.objects.filter(username=username, password= password)
				if not user:
					return JsonResponse({"username":username, "action":action, "status":"fail", "bill id":bill_id})
				user = user[0]
				user.credit += bill.payment
				bill.delete()
				user.save()
				return JsonResponse({"status":"fail", "action":action, "username":username, "bill id":bill_id})
		elif action=="info":
			user = User.objects.filter(username=username, password=password)
			if not user:
				return JsonResponse({"status":"fail", "action":action, "username":username})
			user = user[0]
			return JsonResponse({"status":"success", "action":action,"username":username, "money":user.credit, "user id":user.user_id, "last use":user.last_use})
		else:
			user = user[0]
			return JsonResponse({"username":username, "action":action, "status":"fail"})
	return JsonResponse({"status":401}) 