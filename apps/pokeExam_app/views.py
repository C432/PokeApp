from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Friend
from django.db.models import Q, Count
import bcrypt



def index(request):
    # context = {"users": User.objects.all()}
    return render(request, 'index.html')

def register(request):
    #get user data from post request form
    result = User.objects.validate_registration(request.POST)

    #check for errors in registration validation and create messages / redirect users if so
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        try:
            del request.session['user_id']
        except KeyError:
            pass

        return redirect(index)

    #if no errors in registration validation, redirect user to the welcome page & set post data
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect(dash)

def login(request):
    #get user data from post request form
    result = User.objects.validate_login(request.POST)

    #check for errors in login validation and create messages / redirect users if so
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect(index)

    #if no errors in registration validation, redirect user to the welcome page & set post data
    request.session['user_id'] = result.id
    messages.success(request, "Hello!")
    return redirect(dash)

#logout user
def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect(index)


def dash(request):
    context = {
        'loggedin': User.objects.get(id=request.session['user_id']),
        'friends': Friend.objects.all(),
        'users': User.objects.all().exclude(id=request.session['user_id']),
        'friendNum': User.objects.filter(whofriended__friended=User.objects.get(id=request.session['user_id'])).distinct().annotate(num_friends=Count("whofriended", distinct=True)).filter(whofriended__friended=User.objects.get(id=request.session['user_id']))
    }
    print'dashtest'
    return render(request, 'dash.html', context)

def createFriend(request):
    print '********** FRIEND is working ***********'
    print request.POST
    create = Friend.objects.createFriend(request.POST, request.session['user_id'])
    
    return redirect(dash)

def friendResults(request, user_id):
    print"********* testing friendResults *******"
    context = {
        'user': User.objects.all().get(id=user_id),
        'friends': Friend.objects.all().filter(Q(friender=user_id) | Q(friended=user_id)).order_by('frienddate'),
    }
    return render(request, 'pokeExam_app/friendresults.html', context)
