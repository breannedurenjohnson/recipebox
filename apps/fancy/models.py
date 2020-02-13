from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        FIRST_NAME_REGEX = re.compile('[a-zA-Z]')
        if not FIRST_NAME_REGEX.match(postData['first_name']) or len(postData['first_name']) < 2: 
            errors['valid_first_name'] = "Please enter a valid first name."
            print(errors)
        LAST_NAME_REGEX = re.compile('[a-zA-Z]')
        if not LAST_NAME_REGEX.match(postData['last_name']) or len(postData['last_name']) < 2:
            errors['valid_last_name'] = "Please enter a valid last name."
            print(errors)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['valid_email'] = "Invalid email address."
        users = User.objects.filter(email = postData['email'])
        if len(users) > 0:
            errors['email_duplicate'] = "Email is already taken."
        if len(postData['password']) < 8:
            errors['password_length'] = "Password is too short."
            print(errors)        
        if postData['password'] != postData['password_conf']:
            errors['password_match'] = "Password and password confirmation do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images/')
    recipe = models.TextField(null=True)
    instructions = models.TextField(null=True)
    user = models.ForeignKey(User, related_name="recipes")
    meal = models.CharField(max_length=45)
    users_who_like = models.ManyToManyField(User, related_name="liked_recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title