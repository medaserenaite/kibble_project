from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.kibble_app.models import *

def index(request):
    return render(request,'index.html')

def admin(request):
    return render(request,"admin_login.html")

def register(request):
    check = Admin.objects.register(

        request.POST['firstName'],
        request.POST['lastName'],
        request.POST['email'],
        request.POST['password'],
        request.POST['confirm']
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect ('/admin')
    else:
        messages.add_message(request, messages.SUCCESS, "Thank You for registering. Please Log In")
        return redirect('/admin')

def admin_dashboard(request):

        context = {
        "appointments": Appointment.objects.all(),
        "logged_in": request.session['adminid'],
    } 

        return render(request, "admin_dashboard.html", context)

def login(request):


    check = Admin.objects.login(
    request.POST['email'],
    request.POST['password']
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/admin")
    else:
    
        x = Admin.objects.get(email=request.POST['email'])
        if x.password == request.POST['password']:
            request.session['firstName'] = x.firstName
            request.session['lastName'] = x.lastName
            request.session['loggedin'] = True
            request.session['adminid'] = x.id

        return redirect('/admin_dashboard')

def add_appt(request):
    check = Appointment.objects.validation(request.POST, request)

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect ('/admin_dashboard')
    else:
    
        return redirect('/admin_dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

def update(request,id):
    check = Appointment.objects.editValidation(request.POST, request)
    
    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/edit/'+id)
    else:

        a = Appointment.objects.get(id=id)
        a.patient = request.POST['patient']
        a.reason = request.POST['reason']
        a.date = request.POST['date']
        a.save()
        return redirect('/admin_dashboard')

def destroy(request,id):
    Destroy = Appointment.objects.get(id=id)
    Destroy.delete()
    return redirect('/admin_dashboard')

def approve(request,id):
    approve = Appointment.objects.get(id=id)
    approve.approve = True
    approve.save()
    return redirect('/admin_dashboard')



def edit(request,id):

    context = {
    
        "appointments": Appointment.objects.get(id=id)
    }
    return render (request,'edit.html',context)