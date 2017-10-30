from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
from datetime import datetime
# Create your models here.

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')


class UserManager(models.Manager):
    def validate_registration(self,post_data):
        errors={}
        for field,value in post_data.iteritems():
            if len(value)<1:
                errors[field]="{} field is required".format(field.replace('_',''))
            if field == "first_name" or field =="username":
                if not field in errors and len(value) < 3:
                    errors[field]="{} field must be at least 3 characters".format(field.replace('_',''))
        if post_data['password'] != post_data['confirmpw']:
            errors['password'] = "Password does not match"
        return errors



    def valid_user(self, post_data):
        hashed = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt(5))
        new_user = self.create(
            first_name = post_data['first_name'],
            username= post_data['username'],
            password = hashed
        )
        return new_user
        



    def validate_login(self, post_data):
        errors = {}
        if len(self.filter(username=post_data['username'])) > 0:
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['login']='username/password incorrect'
        else:
            errors['login']='username/password incorrect'
        return errors

    def valid_login(self, post_data):
        if len(self.filter(username=post_data['username'])) > 0:
            user = self.filter(username=post_data['username'])[0]
        return user


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)       # needs add
    updated_at = models.DateTimeField(auto_now=True)           # does not need add
    objects = UserManager()
    def __repr__(self):
        return "first:: {} last:: {} ".format(self.first_name,self.last_name)
###########################################################################################################





class Product(models.Model):
    item_name = models.CharField(max_length = 255)

    my_wish = models.ForeignKey(User, related_name = 'user_wish')
    friend = models.ManyToManyField(User, related_name = 'friend_wish')

    created_at = models.DateTimeField(auto_now_add=True)       # needs add
    updated_at = models.DateTimeField(auto_now=True)   




