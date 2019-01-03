from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0_9.+_-]+\.[a-zA-Z]+$')


class AdminManager(models.Manager):
    def register(self, firstName, lastName, email, password, confirm):
        errors = []
        if len(firstName) < 1:
            errors.append("Must Provide a full first name")
        if len(lastName) < 1:
            errors.append("Must provide a valid last name")
        if len(email) < 1:
            errors.append("An Email is required")
        elif not EMAIL_REGEX.match(email):
            errors.append("Must provide a valid email adress")
        else:
            adminMatchingEmail = Admin.objects.filter(email = email)
            if len(adminMatchingEmail) > 0:
                errors.append("Email already in use")
        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 6:
            errors.append("Password must be at least 6 charaters")
        elif password != confirm:
            errors.append("passwords must match")

        response = {
            "errors": errors,
            "valid": True,
            "admin": None
        }
        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            
            response["admin"] = Admin.objects.create(
            firstName = firstName,
            lastName = lastName, 
            email = email, 
            password = password,
            #password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )        
        return response

    def login(self, email, password):
        errors = []

        if len(email) < 1:
            errors.append('Email is required')
        elif not EMAIL_REGEX.match(email): 
            errors.append('Invalid email')
        else: 
            adminMatchingEmail = Admin.objects.filter(email = email)
            if len(adminMatchingEmail)== 0:
                errors.append("unknown email")
        
        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("password must be at least 8 chars")
        
        response = {

            "errors": errors,
            "valid": True,
            "admin": None
        }

        
        if len(errors) > 0:
            response['errors'] = errors
            response['valid'] = False
        return response
class AppointmentManager(models.Manager):
    def validation(self, postData, request):
        errors = []
        if len(postData['patient']) < 1:
            errors.append("Must Provide a patients full name")
        if len(postData['date']) < 1:
            errors.append("Must provide date")
        if len(postData['reason']) < 1:
            errors.append("reason must be longer than 10 characters")
            
        response = {

            "errors": errors,
            "valid": True,
            "appointment": None
        }
        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            
            response["appointment"] = Appointment.objects.create(
                patient = postData['patient'],
                date = postData['date'],
                reason = postData['reason'],
                uploader = Admin.objects.get(id = request.session['adminid'])
           
            )        
        return response

    def editValidation(self, postData, request):
        errors = []
        if len(postData['patient']) < 1:
            errors.append("Must Provide a patients full name")
        if len(postData['date']) < 1:
            errors.append("Must provide date")
        if len(postData['reason']) < 1:
            errors.append("reason must be longer than 10 characters")
            
        response = {

            "errors": errors,
            "valid": True,
            "appointment": None
        }
        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
            
        return response

class Admin(models. Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)

    objects = AdminManager()


class Appointment(models.Model):
    patient = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    reason = models.CharField(max_length = 255)
    uploader = models.ForeignKey(Admin, related_name="uploader",on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)

    objects = AppointmentManager()
