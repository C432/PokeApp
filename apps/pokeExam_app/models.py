from __future__ import unicode_literals
import bcrypt
import re
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z\s]\w+')
class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for email
        if len(self.filter(alias=post_data['alias'])) > 0:
            # check this user's password
            user = self.filter(alias=post_data['alias'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Password Incorrect!')
        else:
            errors.append('alias not found!')
        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []

        #error handling for name fields
        if len(post_data['name']) < 2:
            errors.append("Names must be at least 3 characters!")

        if len(post_data['alias']) < 2:
            errors.append("alias must be at least 3 characters!")

        #error handling for passwords
        if len(post_data['password']) < 8:
            errors.append("Passwords must be at least 8 characters!")

        # error handling for  letter characters
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Names must contain letter characters only!')

        #error handling for uniqueness of alias
        if len(User.objects.filter(alias=post_data['alias'])) > 0:
            errors.append("This alias is already in use!")

        #error handling for password matches
        if post_data['password'] != post_data['password_confirm']:
            errors.append("Passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw(
                (post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                alias=post_data['alias'],
                email=post_data['email'],
                password=hashed,
            )
            return new_user
        return errors
class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name, self.alias

class FriendManager(models.Manager):
    def createFriend(self, postData, user_id):
        print (postData['dash'])
        self.create(
            friender=User.objects.get(id=user_id),
            friended=User.objects.all().get(name=postData['dash'])
        )
        print '***models test***'
class Friend(models.Model):
    frienddate = models.DateTimeField(auto_now_add=True)
    friender = models.ForeignKey(User, related_name="whofriended")
    friended = models.ForeignKey(User, related_name="gotfriended")
    objects = FriendManager()
    def __repr__(self):
        return "<Friends - friender: {}, friended: {}, frienddate: {}>".format(self.friender, self.friended, self.frienddate)
