
from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse("<h1> Welcome  </h1>")




def dashboard_callback(request, context):
    from accounts.models import User
    from attendance.models import Attendance   # adjust imports

    context.update({
        "stats": [
            {"title": "Total Users",    "metric": User.objects.count(),       "icon": "people"},
            {"title": "Students",       "metric": User.objects.filter(role="student").count(), "icon": "school"},
            {"title": "Teachers",       "metric": User.objects.filter(role="teacher").count(), "icon": "badge"},
            {"title": "Today's Absent", "metric": Attendance.objects.filter(status="absent").count(), "icon": "event_busy"},
        ],
    })
    return context