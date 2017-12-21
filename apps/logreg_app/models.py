# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class UserManager(models.Manager):
    def registration_validation(self, data):
        errors = {}
        if len(data['name']) < 2:
            errors["name"] = "Name needs to be at least 2 characters"

        if len(data['alias']) < 2:
            errors["alias"] = "Alias needs to be at least 2 characters"

        if len(data['password']) < 8:
            errors["password"] = "Password needs to be at least 8 characters"
        
        if not data['password'] == data['confirm']:
            errors["password"] = "Passwords do not match"
        return errors

    def user_validation(self,data):
        errors = {}
        
        existing_user = User.objects.filter(email_address = data['email'])

        if len(existing_user) < 1:
            errors["email"] = "Email does not match our records"

        else:
            print existing_user
            print existing_user[0]
            print existing_user[0].password
            if data['password'] != existing_user[0].password:
                errors["password"] = "Password does not match our records for that email"
        return errors

class User(models.Model):
    name= models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email_address = models.CharField(max_length = 255, unique = True)
    password = models.CharField(max_length = 255)
    # dob = models.DateField(verbose_name=None)
    # message = models.CharField(max_length = 255)
    objects = UserManager()

class Wish_Manager(models.Manager):
    def wish_validation(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors["item"] = "Item cannot be left blank and must be at least 3 characters."
            return errors

class Add_item(models.Model):
    item = models.CharField(max_length=45)
    date_added = models.DateTimeField(auto_now_add=True)
    
    created_by = models.ForeignKey(User, related_name='created_wishes')
    copied_by = models.ManyToManyField(User, related_name='items_copied')
    objects = Wish_Manager()

    def consumers(self):
        return self.copied_by.exclude(id=self.created_by.id)

    

# Create your models here.
